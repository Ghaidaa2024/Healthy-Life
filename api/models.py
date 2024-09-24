from django.db import models
from diet.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from diet.models import BaseModel
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _




class CustomUser(AbstractUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(max_length=50,
                                  null=True,
                                  blank=True)
    last_name = models.CharField(max_length=50,
                                 null=True,
                                 blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return self.username

class Food(BaseModel):
    class Type(models.TextChoices):
        CARBOHYDRATE = '1', 'carbohydrate'
        PROTEIN = '2', 'protein'
        FAT = '3', 'fat'
        FRUITS = '4', 'fruits'
        MILK = '5', 'milk'
        VEGETABLES = '6', 'vegetables'

    class TypeAmount(models.IntegerChoices):
        CUP=1
        GRAM=2
        PIECE=3

    name = models.CharField(max_length=30, unique=True)
    food_type = models.CharField(max_length=2, choices=Type.choices)
    amount = models.PositiveSmallIntegerField(default=0)
    amout_type = models.PositiveSmallIntegerField(choices=TypeAmount.choices, default=2)
    calories = models.FloatField(max_length=30, default=0)
    protein = models.FloatField(max_length=30, default=0)
    fat = models.FloatField(max_length=30, default=0)
    carbohydrate = models.FloatField(max_length=30, default=0)
    calcium = models.FloatField(max_length=30, default=0)
    cholesterol = models.FloatField(max_length=30, default=0)
    iron = models.FloatField(max_length=30, default=0)
    sodium = models.FloatField(max_length=30, default=0)
    vitamin_C = models.FloatField(max_length=30, default=0)
    vitamin_A = models.FloatField(max_length=30, default=0)
    def __str__(self):
        return self.name
    


class BMIRecord(BaseModel):
    name = models.CharField(max_length=30)
    weight = models.FloatField()
    weight_unit = models.CharField(max_length=10)
    height = models.FloatField()
    height_unit = models.CharField(max_length=10)
    bmi = models.FloatField()

    def __str__(self):
        return self.name
    

class Calories(BaseModel):
    class Gender(models.IntegerChoices):
        MAN = 1
        WOMAN = 2

    class WeightPlan(models.IntegerChoices):
        WEIGHT_LOSS = 1
        WEIGHT_GAIN = 2
        WEIGHT_MAINTENANCE = 3

    name = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    age = models.PositiveSmallIntegerField()
    gender = models.PositiveSmallIntegerField(choices= Gender)
    plan = models.PositiveSmallIntegerField(choices=WeightPlan, default=1)
    pal= models.FloatField()

    def __str__(self):
        return self.name.username