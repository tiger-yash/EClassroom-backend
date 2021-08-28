from re import T
from rest_framework import serializers
from authentication.models import Account
from classes.models import Classes,Assignment,Test
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator


class ClassSerializer(serializers.ModelSerializer):

    subject = serializers.CharField(max_length=20)

    class Meta:
        model = Classes
        fields = ('id', 'subject', 'teacher')
        extra_kwargs = {
            'teacher':{'required':False},
 
        }

class AssignmentSerializer(serializers.ModelSerializer):
    assignment = serializers.CharField(max_length=20)
    url = serializers.URLField(max_length=200)
    due_date=serializers.DateTimeField()
    end_date=serializers.DateTimeField()
    class_code=serializers.CharField(max_length=7)
    class Meta:
        model = Assignment
        fields = ('id', 'assignment','due_date','end_date','url')
        extra_kwargs = {
            'end_date':{'required':False},
            'due_date':{'required':False}
        }

class TestSerializer(serializers.ModelSerializer):
    test = serializers.CharField(max_length=20)
    url = serializers.URLField(max_length=200)
    due_date=serializers.DateTimeField()
    end_date=serializers.DateTimeField()

    class Meta:
        model = Test
        fields = ('id', 'test','due_date','end_date','url')
        extra_kwargs = {
            'end_date':{'required':False},
            'due_date':{'required':False}
        }

