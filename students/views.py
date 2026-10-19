from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import StudentForm, CourseForm, ResultForm
from .models import Student, Course, Attendance, Result


class StudentSyncLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    active_students = Student.objects.filter(status='active').count()
    today = date.today()
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='present').count()
    total_marked_today = today_attendance.count()
    attendance_rate_today = round((present_today / total_marked_today) * 100, 1) if total_marked_today else 0

    recent_students = Student.objects.select_related('course').all()[:6]

    courses = Course.objects.all()
    course_labels = [c.name for c in courses]
    course_counts = [c.total_students() for c in courses]

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'active_students': active_students,
        'attendance_rate_today': attendance_rate_today,
        'recent_students': recent_students,
        'course_labels': course_labels,
        'course_counts': course_counts,
    }
    return render(request, 'students/dashboard.html', context)


@login_required
def student_list(request):
    query = request.GET.get('q', '')
    course_filter = request.GET.get('course', '')
    if course_filter in (None, 'None', 'null'):
        course_filter = ''
    students = Student.objects.select_related('course').all()

    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(roll_no__icontains=query) |
            Q(email__icontains=query)
        )
    if course_filter:
        students = students.filter(course_id=course_filter)

    context = {
        'students': students,
        'courses': Course.objects.all(),
        'query': query,
        'course_filter': course_filter,
    }
    return render(request, 'students/student_list.html', context)


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related('course'), pk=pk)
    results = student.results.all()
    attendances = student.attendances.all()[:10]
    context = {
        'student': student,
        'results': results,
        'attendances': attendances,
        'result_form': ResultForm(),
    }
    return render(request, 'students/student_detail.html', context)


@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'{student.full_name()} was added successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated successfully.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student'})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name()
        student.delete()
        messages.success(request, f'{name} was removed from StudentSync.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@login_required
def add_result(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.student = student
            result.save()
            messages.success(request, 'Result added successfully.')
    return redirect('student_detail', pk=student.pk)


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'students/course_list.html', {'courses': courses})


@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'students/course_form.html', {'form': form, 'title': 'Add Course'})


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'students/course_form.html', {'form': form, 'title': 'Edit Course'})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_list')
    return render(request, 'students/course_confirm_delete.html', {'course': course})


@login_required
def attendance_mark(request):
    courses = Course.objects.all()
    course_id = request.GET.get('course') or request.POST.get('course')
    if course_id in (None, '', 'None', 'null'):
        course_id = None

    selected_date = request.GET.get('date') or request.POST.get('date') or str(date.today())
    students = Student.objects.filter(status='active')
    if course_id:
        students = students.filter(course_id=course_id)

    if request.method == 'POST':
        for student in students:
            status_value = request.POST.get(f'status_{student.id}')
            if status_value:
                Attendance.objects.update_or_create(
                    student=student, date=selected_date,
                    defaults={'status': status_value}
                )
        messages.success(request, f'Attendance saved for {selected_date}.')
        return redirect(f"{request.path}?course={course_id or ''}&date={selected_date}")

    existing = {
        a.student_id: a.status for a in Attendance.objects.filter(date=selected_date, student__in=students)
    }

    context = {
        'courses': courses,
        'students': students,
        'selected_course': course_id,
        'selected_date': selected_date,
        'existing': existing,
    }
    return render(request, 'students/attendance.html', context)


@login_required
def attendance_report(request):
    student_id = request.GET.get('student')
    if student_id in (None, '', 'None', 'null'):
        student_id = None
    records = Attendance.objects.select_related('student').all()
    if student_id:
        records = records.filter(student_id=student_id)
    records = records[:200]
    context = {
        'records': records,
        'students': Student.objects.all(),
        'selected_student': student_id,
    }
    return render(request, 'students/attendance_report.html', context)