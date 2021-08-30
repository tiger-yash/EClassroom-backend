from django.db import models
from django.conf import settings


class Assignment(models.Model):
    assignment = models.CharField(max_length=20)
    url = models.URLField(max_length=200)
    start_date = models.DateTimeField(
        verbose_name='date created', auto_now_add=True)
    due_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    max_marks = models.IntegerField(blank=True,default=0)
    def __str__(self):
        return self.assignment


class Test(models.Model):
    test = models.CharField(max_length=20)
    url = models.URLField(max_length=200)
    start_date = models.DateTimeField(
        verbose_name='date created', auto_now_add=True)
    due_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    max_marks = models.IntegerField(blank=True,default=0)
    def __str__(self):
        return self.test


class Classes(models.Model):
    subject = models.CharField(max_length=20,default='Subject')
    class_code = models.CharField(max_length=7,blank=True, unique=True)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="students")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="teacher")
    assignments = models.ManyToManyField(
        Assignment, blank=True, related_name="assignments")
    tests = models.ManyToManyField(Test, blank=True, related_name="tests")

    def __str__(self):
        return self.class_code

    def add_assignment(self, assignment):
        if not assignment in self.assignments.all():
            self.assignments.add(assignment)
            self.save()

    def add_test(self, test):
        if not test in self.tests.all():
            self.tests.add(test)
            self.save()

    def remove_assignment(self,assignment):
        if assignment in self.assignments.all():
            self.assignments.remove(assignment)
            self.save()
    
    def remove_test(self,test):
        if test in self.tests.all():
            self.tests.remove(test)
            self.save()

    def add_student(self,student):
        if not student in self.students.all():
            self.students.add(student)
            self.save()

    def remove_student(self,student):
        if student in self.students.all():
            self.students.remove(student)
            self.save()