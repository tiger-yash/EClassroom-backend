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


class AllClassesView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClassSerializer

    def get(self,request):
        classes=Account.objects.get(id=request.user.id).classes.all()
        
        arr=[]
        for x in classes:
            arr.append({'id':x.id,'subject':x.subject,'class_code':x.class_code,'teacher':x.teacher.username})
        return Response({'classes':arr}, status=status.HTTP_200_OK)

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
        ts_class.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClassView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClassSerializer
    queryset=Classes.objects.all()
    def get(self,request,pk):
        serializer = ClassSerializer(Classes.objects.get(id=pk))
        data=serializer.data
        data['teacher']=Classes.objects.get(id=pk).teacher.username
        data['teacher_email']=Classes.objects.get(id=pk).teacher.email
        data['class_code']=Classes.objects.get(id=pk).class_code
        arr=[]
        for x in Classes.objects.get(id=pk).students.all():
            arr.append({'username':x.username})
        data['students']=arr
        return Response(data, status=status.HTTP_200_OK)

    def delete(self,request,pk):
        ts_class=Classes.objects.get(id=pk)
        Account.remove_class(ts_class)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignmentView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer

    def get(self,request):
        assignments=Classes.objects.get(class_code=request.data['class_code']).assignments.all()
        arr=[]
        for ass in assignments:
            arr.append({'assignment':ass.assignment,'id':ass.id})
        return Response({'assignments':arr}, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            assignment = Assignment.objects.create(assignment=data['assignment'], url=data['url'], due_date=data[
                                                   'due_date'], end_date=data['end_date'],max_marks=data["max_marks"])
            ts_class=Classes.objects.get(class_code=data['class_code'])
            ts_class.add_assignment(assignment)
            data = serializer.data
            data['id']=assignment.id
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user=Account.objects.get(id=request.user.id)
        assignment=Assignment.objects.get(id=request.data['id'])
        if assignment.teacher==user:
            serializer = AssignmentSerializer(Assignment.objects.get(
                id=request.data['id']), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"You do not have permission."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        user=Account.objects.get(id=request.user.id)
        assignment=Assignment.objects.get(id=request.data['id'])
        if assignment.teacher==user:
            ts_class=Classes.objects.get(class_code=request.data['class_code'])
            ts_class.remove_assignment(assignment)
            assignment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"You do not have permission."},status=status.HTTP_400_BAD_REQUEST)

class TestView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TestSerializer

    def get(self,request):
        tests=Classes.objects.get(class_code=request.data['class_code']).tests.all()
        arr=[]
        for test in tests:
            arr.append({'test':test.test,'id':test.id})
        return Response({'tests':arr}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            test = Test.objects.create(test=data['test'], url=data['url'], due_date=data[
                                                   'due_date'], end_date=data['end_date'],max_marks=data["max_marks"])
            ts_class=Classes.objects.get(class_code=data['class_code'])
            ts_class.add_test(test)
            data = serializer.data
            data['id']=test.id
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user=Account.objects.get(id=request.user.id)
        test=Test.objects.get(id=request.data['id'])
        if test.teacher==user:
            serializer = TestSerializer(Test.objects.get(
                id=request.data['id']), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"You do not have permission."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        user=Account.objects.get(id=request.user.id)
        test=Test.objects.get(id=request.data['id'])
        if test.teacher==user:
            ts_class=Classes.objects.get(class_code=request.data['class_code'])
            ts_class.remove_test(test)
            test.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"You do not have permission."},status=status.HTTP_400_BAD_REQUEST)