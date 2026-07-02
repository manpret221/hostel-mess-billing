from rest_framework import serializers
from .models import Student, MealSlot,MealAttendance ,MonthlyBill, GuestMeal

class StudentSerializer(serializers.ModelSerializer):
    username= serializers.CharField(source='user.username',read_only=True)
    
    class Meta:
        model = Student
        fields=['id','username','room_number','joined_date']
        
        
class MealSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model=MealSlot
        fields= ['id' ,'name', 'default_rate']
        


class MealAttendanceSerializer(serializers.ModelSerializer):
        
    meal_name = serializers.CharField(source='meal.name', read_only=True)

    class Meta:
        model=MealSlot
        fields= ['id','date','meal_name','ate']
        
class MonthlyBillSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    
    class Meta:
        Model = MonthlyBill
        fields=['id','student_name','year','month','total_amount','total_meals', 'total_guests']
        
        
class GuestMealSerializer(serializers.ModelSerializer):
    meal_name = serializers.CharField(source='meal.name', read_only=True)
    
    class Meta:
        model = GuestMeal
        fields = ['id', 'date', 'meal_name', 'guest_count']