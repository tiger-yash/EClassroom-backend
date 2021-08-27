from rest_framework import serializers
from authentication.models import Account, GoogleAuth
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=Account.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=Account.objects.all())])
    mode = serializers.CharField(max_length=6,default="local")
    g_token = serializers.CharField(default=None,
         validators=[UniqueValidator(queryset=GoogleAuth.objects.all())])

    class Meta:
        model = Account
        fields = ('id', 'email', 'password', 'username','mode', "g_token","is_teacher","is_student")
        extra_kwargs = {
            'password': {'write_only': True,'required':False},
            'id':  {'required': False, 'read_only': True},
            'g_token':{'required':False,'write_only': True,}
        }

    def create(self, validated_data):
        
        if validated_data["mode"]=="local":
            user = Account.objects.create_user(username=validated_data["username"], email=validated_data["email"], 
             password=validated_data["password"],is_teacher=validated_data["is_teacher"], 
                is_student=validated_data["is_student"])
            authenticate(
                username=validated_data["username"], password=validated_data["password"])
            return user
        else:
            print(validated_data)
            user = Account.objects.create_user(
                username=validated_data["username"],email=validated_data["email"], 
             is_teacher=validated_data["is_teacher"],is_student= validated_data["is_student"])
            GoogleAuth.objects.create(user=user,g_token=validated_data["g_token"])
            return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, default=None)
    mode = serializers.CharField(max_length=6,default="local")
    g_token = serializers.CharField(max_length=100)

    def validate(self, data):
        if data.get('mode')=="local":
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to login :( !")
            return data
        else:
            try:
                user=GoogleAuth.objects.get(g_token=data.get('g_token')).user
                data['user'] = user
                return data
            except:
                raise serializers.ValidationError("Unable to login :( !")
            
                
            

    class Meta:
        model = Account
        fields = ('id', 'username','mode','g_token','password')
        extra_kwargs = {
            'password': {'write_only': True,'required':False},
            'id':  {'required': False, 'read_only': True},
            'g_token':{'required':False,'write_only': True,}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'username')
