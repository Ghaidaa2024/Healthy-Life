# myproject/urls.py

from django.contrib import admin
from django.urls import path
from api import views as frontView
from api.views.views import CaloriesAPI, LoginView, BMIAPI, FoodCalculator

urlpatterns = [
    # path('', frontView.home, name='home'),
    # path('login/', frontView.login_view, name='login'),
    # path('calculateBMI/', frontView.calculateBMI, name='calculateBMI'),
    # path('calories/', frontView.calories_calculator, name='calories'),
    # path('food-calculator/', frontView.food_calculator, name='food_calculator'),
    # path('meals/', frontView.food_meals, name='meals'),
    # path('signup/', frontView.signup_view, name='signup'),
    # path('more_info/', frontView.info_view, name='more_info'),
    path('token/', LoginView.as_view(), name='login'),
    path('bmi/', BMIAPI.as_view(), name = 'bmi'),
    path('FoodCalculator/', FoodCalculator.as_view(), name='FoodCalculator'),
    path('calories/', CaloriesAPI.as_view(), name = 'calories')
]

