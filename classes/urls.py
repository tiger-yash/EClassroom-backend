from classes.models import Assignment
from django.urls import path
from .views import ClassView,AssignmentView,TestView,AllClassesView

urlpatterns = [
    path('', ClassView.as_view()),
    path('<int:pk>/', AllClassesView.as_view()),
    path('assignment/',AssignmentView.as_view()),
    path('test/',TestView.as_view())
]