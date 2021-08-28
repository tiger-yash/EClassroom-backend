from rest_framework import serializers, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ClassSerializer, AssignmentSerializer, TestSerializer)
from authentication.models import Account
from classes.models import Assignment, Classes,Test
import string
import secrets


class ClassView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClassSerializer

    def post(self, request):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            teacher = Account.objects.get(id=request.user.id)
            ts_class = Classes.objects.create(
                teacher=teacher, subject=request.data['subject'])
            data = serializer.data
            alphabet = string.ascii_letters + string.digits

            class_code=''.join(secrets.choice(alphabet) for i in range(7))
            ts_class.class_code=class_code
            ts_class.save()
            teacher.add_class(ts_class)
            data['class_code']=class_code
            
            data['id']=ts_class.id
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        ts_class=Classes.objects.get(class_code=request.data['class_code'])
        Account.remove_class(ts_class)

class AssignmentView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer

    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            assignment = Assignment.objects.create(assignment=data['assignment'], url=data['url'], due_date=data[
                                                   'due_date'], end_date=data['end_date'])
            ts_class=Classes.objects.get(class_code=data['class_code'])
            ts_class.add_test(assignment)
            data = serializer.data
            data['id']=assignment.id
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = AssignmentSerializer(Assignment.objects.get(
            id=request.data['id']), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        assignment=Assignment.objects.get(id=request.data['id'])
        ts_class=Classes.objects.get(class_code=request.data['class_code'])
        ts_class.remove_assignment(assignment)
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TestSerializer

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            test = Test.objects.create(test=data['test'], url=data['url'], due_date=data[
                                                   'due_date'], end_date=data['end_date'])
            ts_class=Classes.objects.get(class_code=data['class_code'])
            ts_class.add_test(test)
            data = serializer.data
            data['id']=test.id
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = TestSerializer(Test.objects.get(
            id=request.data['id']), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        test=Test.objects.get(id=request.data['id'])
        ts_class=Classes.objects.get(class_code=request.data['class_code'])
        ts_class.remove_test(test)
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)