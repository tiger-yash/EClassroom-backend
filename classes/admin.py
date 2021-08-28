from django.contrib import admin
from classes.models import Classes,Tests,Assignments
# Register your models here.
admin.site.register(Classes)
admin.site.register(Assignments)
admin.site.register(Tests)