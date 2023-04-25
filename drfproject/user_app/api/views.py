from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user_app.api.serializers import RegistrationSerializer
from user_app import models
from rest_framework_simplejwt.tokens import RefreshToken



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout_view(request):
#     user=request.user
#     try:
#         token=Token.objects.get(user=user)
#         token.delete()
#         return Response({'message':'Authentication token deleted successfully.'})
#     except Token.DoesNotExist:
#         return Response({'error':'Authenticated token not found. '},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST',])
def logout_view(request):
    if request.method=='POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    if request.method=='POST':
        serializer=RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            
            data['response']="Registration Successful!"
            data['username']=account.username
            data['email']=account.email
            # token=Token.objects.get(user=account).key
            # data['token']=token
            refresh=RefreshToken.for_user(account)
            data['token']={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
        else:
            data=serializer.errors    
        return Response(data)