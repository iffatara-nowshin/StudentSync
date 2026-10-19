from django.contrib import admin
from .models import Course, Student, Attendance, Result


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'duration_years', 'total_students')
    search_fields = ('name', 'code')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'first_name', 'last_name', 'course', 'status', 'admission_date')
    list_filter = ('status', 'course', 'gender')
    search_fields = ('roll_no', 'first_name', 'last_name', 'email')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam_name', 'subject', 'marks_obtained', 'total_marks')
    list_filter = ('exam_name', 'subject')
