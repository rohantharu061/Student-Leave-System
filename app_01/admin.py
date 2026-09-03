from django.contrib import admin
from .models import StudentLeave

# Register your models here.
@admin.register(StudentLeave)
class StudentLeaveAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'roll_number',
        'full_name',
        'faculty',
        'semester',
        'start_date',
        'end_date',
        'Leave_type',
        'reason',
        'guardian_contact',
        'student_mail',
    )