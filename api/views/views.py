from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from api.exceptions import *
from api.models import *
from django.core import signing
signer = signing.TimestampSigner()
from django.http import JsonResponse
from api.models import BMIRecord
from api.serializers import FoodSerializer
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class LoginView(APIView):
    def InputSerializer(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise InputException(detail='Missing Parameters')

        return username, password

    def OutputSerializer(self, token, username):
        return {'token': token}

    def post(self, request):
        username, password = self.InputSerializer(request)

        user = CustomUser.objects.filter(username__iexact=username)
        if user:
            user=user[0]
            if check_password(password, user.password):
                token_payload = {'id': str(user.id)}
                token_value = signer.sign_object(token_payload)
                response_data = self.OutputSerializer(token_value, username)

                return Response(response_data)
        else:
            return Response ('Not Found', status=status.HTTP_404_NOT_FOUND)

class BMIAPI(APIView):
    result = None
    def post(self, request):
        data = request.data
        name = data.get('name', None)
        weight = data.get('weight', None)
        weight_unit = data.get('weight_unit', None)
        height = data.get('height', None)
        height_unit = data.get('height_unit', None)
        
        if weight_unit == 'lbs':
            weight = float(weight) * 0.453592  # Convert pounds to kilograms
        else:
            weight = float(weight)
        
        if height_unit == 'inch':
            height = float(height) * 0.0254  # Convert inches to meters
        elif height_unit == 'cm':
            height = float(height) / 100  # Convert centimeters to meters
        else:
            height = float(height)
        
        bmi = weight / (height ** 2)

        # Save the record
        BMIRecord.objects.create(name=name, weight=weight, weight_unit=weight_unit, height=height, height_unit=height_unit, bmi=bmi)

        # Determine BMI category and recommendation
        bmi_result = ""
        bmi_recommendation = ""
        bmi = round(bmi,1)
        if bmi < 18.5:
            minimum_weight = 18.5 * (height ** 2)
            maximum_weight = 24.9 * (height ** 2)
            bmi_result = "وزن منخفض"
            bmi_recommendation = f"{round(minimum_weight,2)} kg - {round(maximum_weight,2)} kg "
        
        elif 18.5 <= bmi <= 24.9:
            bmi_result = "وزن طبيعي"
            bmi_recommendation = "You have a normal weight."
        
        elif 25 <= bmi <= 29.9:
            minimum_weight = 18.5 * (height ** 2)
            maximum_weight = 24.9 * (height ** 2)
            bmi_result = "وزن زائد"
            bmi_recommendation = f"{round(maximum_weight,2)} kg - {round(minimum_weight,2)} kg "
            
        elif 30 <= bmi <= 34.9:
            minimum_weight = 18.5 * (height ** 2)
            maximum_weight = 24.9 * (height ** 2)
            bmi_result = "سمنه"
            bmi_recommendation = f" {round(maximum_weight,2)} kg - {round(minimum_weight,2)} kg "
        else:
            minimum_weight = 18.5 * (height ** 2)
            maximum_weight = 24.9 * (height ** 2)
            bmi_result = " سمنه مفرطة"
            bmi_recommendation = f" {round(maximum_weight,2)} kg - {round(minimum_weight,2)} kg "

        result = bmi
        return Response({
            'weight' :weight,
            'bmi': result,
            'Recommendation': bmi_recommendation,
            'Result': bmi_result
        })
    

class CaloriesAPI(APIView):
    def post(self, request):
    #     user = CustomUser.objects.filter(email = userEmail)
        weight = request.data.get('weight', None)
        height = request.data.get('height', None)
        age = request.data.get('age', None)
        gender = request.data.get('gender', None)
        plan = request.data.get('plan', None)
        pal = request.data.get('pal', None)
        
        if not (weight and height and age and gender and plan):
            return Response({'detail': 'Missing Parameters'}, status=status.HTTP_400_BAD_REQUEST)

        weight = float(weight)
        height = float(height)
        age = int(age)
        # Gender mapping
        if gender == 'male':
            gender_value = Calories.Gender.MAN
        elif gender == 'female':
            gender_value = Calories.Gender.WOMAN
        else:
            return Response({'detail': 'Invalid gender value'}, status=status.HTTP_400_BAD_REQUEST)

        # Plan mapping
        if plan == 'lose_weight':
            plan_value = Calories.WeightPlan.WEIGHT_LOSS
        elif plan == 'weight_gain':
            plan_value = Calories.WeightPlan.WEIGHT_GAIN
        else:
            plan_value = Calories.WeightPlan.WEIGHT_MAINTENANCE

        # Caloric calculation
        if gender_value == Calories.Gender.MAN:
            calories = 66 + (weight * 13.7) + (height * 5) - (age * 6.8)
        else:
            calories = 655 + (weight * 9.6) + (height * 1.8) - (age * 4.7)

        cal = calories * float(pal)
      
        if plan_value == 1:
            cal -= 250
        elif plan_value == 2:
            cal += 250
        else:
            cal =cal
        user = CustomUser.objects.filter()
        user = user[0]
       
            # Create a new Calories entry
        Calories.objects.create(name=user, weight=weight, height=height, age=age, gender=gender_value, pal=pal, plan=plan_value)
            
        return Response({'calories': round(cal, 2)})
        

class FoodCalculator(APIView):
    def get(self, request):
        food_type = request.GET.get('food_type', None)
        print(food_type)
        # Mapping from food type name to the database value
        food_type_mapping = {
            'carbohydrate': '1',
            'protein': '2',
            'fat': '3',
            'fruits': '4',
            'milk': '5',
            'vegetables': '6',
        }

        # Get the database value based on the food type name
        db_food_type = food_type_mapping.get(food_type)

        if db_food_type:
            foodObj = Food.objects.filter(food_type=db_food_type) 
        else:
            foodObj = None

        serializer = FoodSerializer(foodObj, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)



