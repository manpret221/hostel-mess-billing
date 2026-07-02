from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    joined_date = models.DateField(auto_now_add=True)
    
    def __str__(self): 
        return self.user.username
    


class MealSlot(models.Model): 
    name = models.CharField(max_length=20, unique=True)
    default_rate = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.name
    
    
class MealAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meal = models.ForeignKey(MealSlot, on_delete=models.CASCADE)
    date = models.DateField()
    ate = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('student','meal' , 'date')
        
    def __str__(self):
        return f"{self.student} - {self.meal} - {self.date}"
    
class MessExpense(models.Model):
    meal= models.ForeignKey(MealSlot,on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)  # NEW

    
    class Meta:
        unique_together = ('meal' , 'date')
    
    def __str__(self):
        return f"{self.date} - {self.meal} - Rs.{self.rate} ({self.description})"
    


class GuestMeal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meal = models.ForeignKey(MealSlot, on_delete=models.CASCADE)
    date = models.DateField()
    guest_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.student} added {self.guest_count} guest(s) - {self.meal} - {self.date}"
    
    
class MonthlyBill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_meals = models.IntegerField()  
    total_guests = models.IntegerField() 
    
    class Meta:
        unique_together = ('student', 'year', 'month')
    
    def __str__(self):
        return f"{self.student} - {self.year}/{self.month} - Rs.{self.total_amount}"