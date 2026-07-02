from django.shortcuts import render

from django.db.models import Sum, Q
from decimal import Decimal
from datetime import datetime, date
from .models import Student, MealAttendance, GuestMeal, MessExpense, MealSlot






from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Student, MealSlot, MealAttendance, MonthlyBill, GuestMeal
from .serializers import (
    StudentSerializer, MealSlotSerializer, MealAttendanceSerializer,
    MonthlyBillSerializer, GuestMealSerializer
)






def get_meal_rate(meal, date):
    """
    Ek specific meal ke liye rate nikalo us din.
    
    Logic:
    1. Pehle MessExpense mein dekho agar us meal+date ke liye special rate hai
    2. Agar nahi, toh MealSlot mein se default_rate use karo
    
    Returns: Decimal (rate in rupees)
    """
    # Special rate check karo
    special_rate = MessExpense.objects.filter(
        meal=meal,
        date=date
    ).first()
    
    if special_rate:
        return special_rate.rate  # Special rate use karo
    else:
        return meal.default_rate  # Default use karo


def calculate_student_monthly_bill(student, year, month):
    """
    Ek student ka ek mahine ka poora bill calculate karo.
    
    Kya karta hai:
    1. Student ne kitne meals khaye (MealAttendance mein ate=True)
    2. Student ke guests ne kitne meals khaye (GuestMeal mein count)
    3. Har meal+date ke liye rate nikalo
    4. Sum karo aur return total bill
    
    Returns: Dictionary with breakdown
    """
    
    bill_details = {
        'student': student,
        'year': year,
        'month': month,
        'total_bill': Decimal('0.00'),
        'meals': []  # breakdown ke liye
    }
    
    # Step 1: Student ke apne meals (Student ne khud khaya)
    student_meals = MealAttendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month,
        ate=True
    )
    
    for attendance in student_meals:
        meal = attendance.meal
        meal_date = attendance.date
        rate = get_meal_rate(meal, meal_date)
        
        meal_entry = {
            'date': meal_date,
            'meal': meal.name,
            'type': 'self',  # khud khaya
            'count': 1,
            'rate': rate,
            'total': rate * 1
        }
        bill_details['meals'].append(meal_entry)
        bill_details['total_bill'] += meal_entry['total']
    
    # Step 2: Guest meals (Guests student ke bill mein charge hote hain)
    guest_meals = GuestMeal.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    )
    
    for guest in guest_meals:
        meal = guest.meal
        meal_date = guest.date
        guest_count = guest.guest_count
        rate = get_meal_rate(meal, meal_date)
        
        meal_entry = {
            'date': meal_date,
            'meal': meal.name,
            'type': 'guest',  # guests
            'count': guest_count,
            'rate': rate,
            'total': rate * guest_count
        }
        bill_details['meals'].append(meal_entry)
        bill_details['total_bill'] += meal_entry['total']
    
    return bill_details


def save_student_monthly_bill(student, year, month):
    """
    Calculate bill aur MonthlyBill table mein save karo.
    
    Kya karta hai:
    1. calculate_student_monthly_bill() se detailed bill nikalo
    2. Total meals aur guests count karo
    3. MonthlyBill table mein entry create/update karo
    4. Return MonthlyBill object
    """
    from .models import MonthlyBill
    
    # Step 1: Calculate bill (pehle wala function use karo)
    bill_details = calculate_student_monthly_bill(student, year, month)
    
    # Step 2: Count meals aur guests
    total_meals = 0
    total_guests = 0
    
    for meal in bill_details['meals']:
        if meal['type'] == 'self':
            total_meals += meal['count']
        elif meal['type'] == 'guest':
            total_guests += meal['count']
    
    # Step 3: MonthlyBill mein save karo (ya update karo agar pehle se exist kare)
    monthly_bill, created = MonthlyBill.objects.update_or_create(
        student=student,
        year=year,
        month=month,
        defaults={
            'total_amount': bill_details['total_bill'],
            'total_meals': total_meals,
            'total_guests': total_guests,
        }
    )
    
    return monthly_bill



class StudentViewSet(viewsets.ModelViewSet):
    # student see his data"
    queryset = Student.objects.all()
    serializer_class= StudentSerializer
    permission_classes = [IsAuthenticated]
    
    
    @action(detail=False,methods=['get'])
    def me(self,request):
        "loggd in student see there data"
        try:
            student = Student.objects.get(user=request.user)
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        
        except Student.DoesNotExist :
            return Response({'error' : "Student Profile NOt Found"} , status = status.HTTP_404_NOT_FOUND)
        
        
class MealAttendanceViewSet(viewsets.ModelViewSet):
    # Mark your attence or see"
    queryset = MealAttendance.objects.all()
    serializer_class = MealAttendanceSerializer
    permission_classes = [IsAuthenticated]
    
    
    
    @action(detail=False , methods=['get'])
        #   Attendance history
    def my_attendance(self,request):
        try:
            student = Student.objects.get(user=request.user)
            attendance = MealAttendance.objects.filter(student=student).order_by('-date')
            serializer = self.get_serializer(attendance, many = True)
            return Response(serializer.data)
        except  Student.DoesNotExist:
            return Response({'error' : 'Student Profile Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
class MealSlotViewSet(viewsets.ReadOnlyModelViewSet):
    #  Availble meal (read-only) 
    queryset = MealSlot.objects.all()
    serializer_class = MealSlotSerializer
    


class GuestMealViewSet(viewsets.ModelViewSet):
    # "guest meal trace"
    queryset = GuestMeal.objects.all()
    serializer_class = GuestMealSerializer
    permission_classes = [IsAuthenticated]
    
    
class MonthlyBillViewSet(viewsets.ReadOnlyModelViewSet):
    # Bills dekho (read-only)
    queryset = MonthlyBill.objects.all()
    serializer_class = MonthlyBillSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_bills(self, request):
        """Logged-in student ke apne bills"""
        try:
            student = Student.objects.get(user=request.user)
            bills = MonthlyBill.objects.filter(student=student).order_by('-year', '-month')
            serializer = self.get_serializer(bills, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)