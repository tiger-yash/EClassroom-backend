from re import T
from rest_framework import serializers
from authentication.models import Account
from classes.models import Classes,Assignment,Test
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator


class ClassesSerializer(serializers.ModelSerializer):

    class_code = serializers.CharField(max_length=7)

    class Meta:
        model = Classes
        fields = ('id', 'class_code')
        extra_kwargs = {
            'students':{'required':False},
        }

class AssignmentsSerializer(serializers.ModelSerializer):

    url = serializers.URLField(max_length=200)

    class Meta:
        model = Assignment
        fields = ('id','url')
        

class TestsSerializer(serializers.ModelSerializer):

    url = serializers.URLField(max_length=200)

    class Meta:
        model = Test
        fields = ('id','url')
        

class MarksSerializer(serializers.ModelSerializer):
    marks=serializers.DecimalField(max_digits=3,decimal_places=2)
    username=serializers.CharField(max_length=30)
    type=serializers.CharField(max_length=10)