from rest_framework import serializers, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer)
from authentication.models import Account



def create_auth_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token

class RegisterView(generics.CreateAPIView):
    permission_classes=[]
    serializer_class = RegisterSerializer
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            token=create_auth_token(serializer.instance)
            
            return Response({'token':token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    permission_classes=[]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = create_auth_token(serializer.validated_data['user'])
            data=serializer.data;
            data['token']=token.key;
            data['username']=serializer.validated_data['user'].username
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.GenericAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = UserSerializer
    
    
    def get(self,request):
        serializer=UserSerializer(Account.objects.get(id=request.user.id))
        return Response(serializer.data)

    def put(self,request):
        serializer=UserSerializer(Account.objects.get(id=request.user.id),data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        profile=Account.objects.get(id=request.user.id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
