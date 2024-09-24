
from api.exceptions import AuthenticationException
from django.core import signing
signer = signing.TimestampSigner()
from api.models import CustomUser


def LoginService(*, username):
    user = CustomUser.objects.filter(username__iexact=username[0])
    if not user:
        raise AuthenticationException()
    user = user[0]
    tokenPayload = {'id':str(user.id)}
    tokenValue = signer.sign_object(tokenPayload) #sign token

    return tokenValue