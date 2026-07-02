from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import(

    StudentViewSet, MonthlyBillViewSet, MealAttendanceViewSet,
    MealSlotViewSet , GuestMealViewSet
                   
    )
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student' )
router.register(r'bills', MonthlyBillViewSet, basename='bill' )
router.register(r'attendance', MealAttendanceViewSet, basename='attendance' )
router.register(r'meals', MealSlotViewSet, basename='meal' )
router.register(r'guests', GuestMealViewSet, basename='guest' )


urlpatterns = [
    path('', include(router.urls)),
]