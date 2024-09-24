from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from api.exceptions import *
from django.core import signing
signer = signing.TimestampSigner()
from django.http import JsonResponse
from api.models import BMIRecord


class LoginView(APIView):
    def InputSerializer(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise InputException(detail='Missing Parameters')

        return username, password

    def OutputSerializer(self, token, username):
        return {'token': token, 'username': username}

    def post(self, request):
        username, password = self.InputSerializer(request)
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationException()

        token_payload = {'id': str(user.id)}
        token_value = signer.sign_object(token_payload)
        response_data = self.OutputSerializer(token_value, username)

        return Response(response_data)



class BMIAPI(APIView):
    result = None
    def post(self, request):
    
        data = request.data
        weight = data.get('weight', None)
        weight_unit = data.get('weight_unit', None)
        height = data.get('height', None)
        height_unit = data.get('height_unit', None)
            
            
        if weight_unit == 'lbs' and height_unit == 'inch':
            bmi = (weight * 703) / (height ** 2)
        else:
            if height_unit == 'cm':
                height = height / 100  # تحويل الطول من سم إلى متر
                bmi = weight / (height ** 2)

        bmi = round(bmi, 2)

 
        BMIRecord.objects.create(weight=weight, weight_unit=weight_unit, height=height, height_unit=height_unit, bmi=bmi)
        print(f'BMI calculated: {bmi}')

        result = bmi
        
        return Response({'bmi': result})