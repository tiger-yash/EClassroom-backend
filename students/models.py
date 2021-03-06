from django.db import models
from django.conf import settings
from classes.models import Test,Assignment

class AssignmentsSubmission(models.Model):
    student=models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="student_ass")
    assignment=models.ForeignKey(
        Assignment,on_delete=models.CASCADE, related_name="assign")
    submission_date=models.DateTimeField(auto_now=True)
    url=models.URLField(max_length=200)
    marks=models.DecimalField(blank=True,max_digits=3,decimal_places=2,default=-1)
    def __str__(self):
        return self.assignment

class TestsSubmission(models.Model):
    student=models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="student_test")
    test=models.ForeignKey(
        Test,on_delete=models.CASCADE, related_name="quiz")
    submission_date=models.DateTimeField(auto_now=True)
    url=models.URLField(max_length=200)
    marks=models.DecimalField(default=-1,blank=True,max_digits=3,decimal_places=2)
    def __str__(self):
        return self.test