from django.db import models
from django.conf import settings


class Assignments(models.Model):
    assignment = models.CharField(max_length=20)
    url = models.URLField(max_length=200)
    start_data = models.DateTimeField(
        verbose_name='date created', auto_now_add=True)
    due_date = models.DateTimeField(blank=True)
    end_data = models.DateTimeField(blank=True)

    def __str__(self):
        return self.assignment


class Tests(models.Model):
    test = models.CharField(max_length=20)
    url = models.URLField(max_length=200)
    start_data = models.DateTimeField(
        verbose_name='date created', auto_now_add=True)
    due_date = models.DateTimeField(blank=True)
    end_data = models.DateTimeField(blank=True)

    def __str__(self):
        return self.test


class Classes(models.Model):
    subject_code = models.CharField(max_length=5)
    class_code = models.CharField(max_length=7, unique=True)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="students")
    teachers = models.OneToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="teacher")
    assignments = models.ManyToManyField(
        Assignments, blank=True, related_name="assignments")
    tests = models.ManyToManyField(Tests, blank=True, related_name="tests")

    def __str__(self):
        return self.batch_code

    def add_assignement(self, assignment):
        if not assignment in self.assignments.all():
            self.assignments.add(assignment)
            self.save()

    def add_tests(self, test):
        if not test in self.tests.all():
            self.tests.add(test)
            self.save()
