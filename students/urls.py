from students.models import AssignmentsSubmission
from classes.models import Assignment
from django.urls import path
from .views import ClassesView,AssignmentsSubmissionView,TestsSubmissionView,CalendarView

urlpatterns = [
    path('class/', ClassesView.as_view()),
    path('assignment/<int:pk>',AssignmentsSubmissionView.as_view()),
    path('test/<int:pk>',TestsSubmissionView.as_view()),
    path('calendar/',CalendarView.as_view())
]