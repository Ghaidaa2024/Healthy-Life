# from django.core import signing
# from django.conf import settings
# from django.http import JsonResponse
# from rest_framework import status
# from api.models import CustomUser
# import logging

# logger = logging.getLogger('dwLogger')

# def validateToken(get_response):
#     def middleware(request):
#         # Skip token validation for these paths
#         if request.path.endswith('token/') or request.path.startswith('/admin') or request.path.endswith('calories/') or request.path.endswith('bmi/'):
#             return get_response(request)

#         # Define signer and token parameters
#         signer = signing.TimestampSigner()
#         token_age_in_minutes = getattr(settings, 'ACCESS_TOKEN_MAX_AGE_IN_MINUTES', 720)

#         try:
#             token = request.META['HTTP_AUTHORIZATION'].split(' ')
#             token = token[1]
#             payload = signer.unsign_object(token, max_age=token_age_in_minutes*60)
#             # username = payload['username']
#             userId = payload['id']
#             customUser= CustomUser.objects.filter(id =userId)
      
#             if not customUser[0]:
#                 logger.error('Invalid Credentials: No user found')
#                 return JsonResponse({
#                                 "message": "Invalid Credentials",
#                                 "extra": {
#                                     "detail": "Invalid Credentials"
#                                 }
#                             }, status=status.HTTP_400_BAD_REQUEST)
#             request.email = customUser[0].email
#         except Exception as e:
#             logger.debug('Invalid Credentials : {}'.format(str(e)))
#             return JsonResponse({
#                                 "message": "Invalid Credentials",
#                                 "extra": {
#                                     "detail": "Invalid Credentials"
#                                 }
#                             }, status=status.HTTP_401_UNAUTHORIZED)
                
#         response = get_response(request)
#         return response

#     return middleware
