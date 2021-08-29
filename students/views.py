from rest_framework import serializers, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ClassesSerializer, AssignmentsSerializer, TestsSerializer)
from authentication.models import Account
from classes.models import Assignment, Classes,Test
from students.models import AssignmentsSubmission, TestsSubmission
from django.db import models

class ClassesView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClassesSerializer

    def post(self,request):
        serializer = ClassesSerializer(data=request.data)
        if serializer.is_valid():
            student = Account.objects.get(id=request.user.id)
            try:
                ts_class = Classes.objects.get(class_code=request.data['class_code'])
                ts_class.add_student(student)
                student.add_class(ts_class)
                data=serializer.data
                data['teacher']=ts_class.teacher.username
                data['subject']=ts_class.subject
                arr=[]
                for x in ts_class.students.all():
                    arr.append({'username':x.username})
                data['students']=arr
                return Response(data, status=status.HTTP_200_OK)
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        
        student = Account.objects.get(id=request.user.id)
        ts_class = Classes.objects.get(class_code=request.data['class_code'])
        ts_class.remove_student(student)
        student.remove_class(ts_class)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignmentsSubmissionView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentsSerializer

    def get(self,request,pk):
        ass=Assignment.objects.get(id=pk)
        data={}
        data['assignment']=ass.test
        data['url']=ass.url
        data['due_date']=ass.due_date
        data['end_date']=ass.end_date
        return Response(data, status=status.HTTP_200_OK)

    def post(self,request,pk):
        serializer = AssignmentsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                assignment=Assignment.objects.get(id=pk)
                student=Account.objects.get(id=request.user.id)
                submission=AssignmentsSubmission.objects.get(assignment=assignment,student=student)
                submission.url=request.data['url']
                submission.save()
            except:
                assignment=Assignment.objects.get(id=pk)
                student=Account.objects.get(id=request.user.id)
                submission=AssignmentsSubmission.objects.create(assignment=assignment,student=student,url=request.data['url'])
            data=serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class TestsSubmissionView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TestsSerializer

    def get(self,request,pk):
        test=Test.objects.get(id=pk)
        data={}
        data['test']=test.test
        data['url']=test.url
        data['due_date']=test.due_date
        data['end_date']=test.end_date
        return Response(data, status=status.HTTP_200_OK)

    def post(self,request,pk):
        serializer =TestsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                test=Test.objects.get(id=pk)
                student=Account.objects.get(id=request.user.id)
                submission=TestsSubmission.objects.get(test=test,student=student)
                submission.url=request.data['url']
                submission.save()
            except:
                test=Test.objects.get(id=pk)
                student=Account.objects.get(id=request.user.id)
                submission=AssignmentsSubmission.objects.create(test=test,student=student,url=request.data['url'])
            data=serializer.data
            data['submission_date']=submission.submission_date
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CalendarView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        student=Account.objects.get(id=request.user.id)
        data={}
        arr1=[]
        arr2=[]
        for ts_class in student.classes.all():
            for test in ts_class.tests.all():
                arr1.append({'test':test.test,'due_date':test.due_date,'subject':ts_class.subject,'id':test.id})
            for assignment in ts_class.assignments.all():
                arr2.append({'assignment':assignment.assignment,'due_date':assignment.due_date,'subject':ts_class.subject,'id':assignment.id})
        data['tests']=arr1
        data['assignments']=arr2
        return Response(data, status=status.HTTP_200_OK)
