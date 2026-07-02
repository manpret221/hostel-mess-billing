from django.contrib import admin
from .models import Student , MealSlot , MealAttendance , MessExpense , GuestMeal,MonthlyBill

# Register your models here.
@admin.register(Student)
class  StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_number', 'joined_date']
    search_fields = [ 'users__username','room_number']
    
    
@admin.register(MealSlot)
class MealSlotAdmin(admin.ModelAdmin):
    list_display = ['name' , 'default_rate']
    
@admin.register(MealAttendance)
class MealAttendance(admin.ModelAdmin):
    list_display = ['student','meal','date','ate']
    list_filter = ['meal','date','ate']
    search_fields = ['students__user__username']
    date_hierarchy = 'date'
    
    
@admin.register(MessExpense)
class MessExpenseAdmin(admin.ModelAdmin):
    list_display = ['meal', 'date' , 'rate' ,'description' ]
    list_filter = [ 'meal','date']
    search_fields = ['description']
    date_hierarchy = 'date'
    
    
@admin.register(GuestMeal)
class GuestMealAdmin(admin.ModelAdmin):
    list_display = [ 'student','meal','date','guest_count']
    list_filter = ['meal','date']
    search_fields = ['student__user__username']
    date_hierarchy = 'date'
    
@admin.register(MonthlyBill)
class MonthlyBillAdmin(admin.ModelAdmin):
    list_display = ['student','year','month','total_amount','total_meals','total_guests'] 
    list_filter = ['year','month']
    search_fields = ['student__user__username']
    readonly_fields = ['total_amount', 'total_meals', 'total_guests']   