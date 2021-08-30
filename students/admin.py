from django.contrib import admin
from students.models import AssignmentsSubmission,TestsSubmission
# Register your models here.
admin.site.register(AssignmentsSubmission)
admin.site.register(TestsSubmission)