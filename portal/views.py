from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict
import json
from datetime import datetime, timedelta

from .models import (
    Student, Teacher, Parent, Class, Subject, Assignment, AssignmentSubmission,
    Grade, Attendance, ProgressReport, Communication, Term, AcademicYear,
    UserProfile, PortalSettings
)
from .forms import (
    LoginForm, AssignmentForm, AssignmentSubmissionForm, GradeForm,
    AttendanceForm, MessageForm, ProfileForm
)

# Utility functions
def is_student(user):
    return hasattr(user, 'userprofile') and user.userprofile.user_type == 'student'

def is_teacher(user):
    return hasattr(user, 'userprofile') and user.userprofile.user_type == 'teacher'

def is_parent(user):
    return hasattr(user, 'userprofile') and user.userprofile.user_type == 'parent'

def get_current_term():
    return Term.objects.filter(is_current=True).first()

def get_current_academic_year():
    return AcademicYear.objects.filter(is_current=True).first()

# Authentication views
def portal_login(request):
    """Login view for the portal"""
    if request.user.is_authenticated:
        return redirect('portal:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('portal:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'portal/login.html', {'form': form})

@login_required
def portal_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('portal:login')

@login_required
def portal_dashboard(request):
    """Main dashboard that redirects based on user type"""
    if not hasattr(request.user, 'userprofile'):
        messages.error(request, 'Your account is not properly configured. Please contact administration.')
        return redirect('portal:logout')
    
    user_type = request.user.userprofile.user_type
    
    if user_type == 'student':
        return student_dashboard(request)
    elif user_type == 'teacher':
        return teacher_dashboard(request)
    elif user_type == 'parent':
        return parent_dashboard(request)
    elif user_type == 'admin':
        return admin_dashboard(request)
    else:
        messages.error(request, 'Unknown user type. Please contact administration.')
        return redirect('portal:logout')

# Student views
@login_required
@user_passes_test(is_student, login_url='portal:login')
def student_dashboard(request):
    """Student dashboard"""
    try:
        student = Student.objects.get(profile__user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('portal:logout')
    
    current_term = get_current_term()
    
    # Get recent assignments
    recent_assignments = Assignment.objects.filter(
        class_obj=student.current_class,
        status='published'
    ).order_by('-due_date')[:5]
    
    # Get recent grades
    recent_grades = Grade.objects.filter(
        student=student,
        term=current_term
    ).order_by('-date_recorded')[:5] if current_term else []
    
    # Get attendance summary
    if current_term:
        attendance_data = Attendance.objects.filter(
            student=student,
            date__range=[current_term.start_date, current_term.end_date]
        ).values('status').annotate(count=Count('id'))
        attendance_summary = {item['status']: item['count'] for item in attendance_data}
    else:
        attendance_summary = {}
    
    # Get unread messages
    unread_messages = Communication.objects.filter(
        recipients=request.user
    ).exclude(read_by=request.user).count()
    
    context = {
        'student': student,
        'current_term': current_term,
        'recent_assignments': recent_assignments,
        'recent_grades': recent_grades,
        'attendance_summary': attendance_summary,
        'unread_messages': unread_messages,
    }
    
    return render(request, 'portal/student/dashboard.html', context)

@login_required
@user_passes_test(is_student, login_url='portal:login')
def student_profile(request):
    """Student profile view"""
    student = get_object_or_404(Student, profile__user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=student.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('portal:student_profile')
    else:
        form = ProfileForm(instance=student.profile)
    
    context = {
        'student': student,
        'form': form,
    }
    
    return render(request, 'portal/student/profile.html', context)

@login_required
@user_passes_test(is_student, login_url='portal:login')
def student_grades(request):
    """Student grades view"""
    student = get_object_or_404(Student, profile__user=request.user)
    current_term = get_current_term()
    
    # Get all terms for the current academic year
    current_year = get_current_academic_year()
    terms = Term.objects.filter(academic_year=current_year) if current_year else []
    
    selected_term_id = request.GET.get('term', current_term.id if current_term else None)
    selected_term = get_object_or_404(Term, id=selected_term_id) if selected_term_id else current_term
    
    # Get grades for selected term
    grades = Grade.objects.filter(
        student=student,
        term=selected_term
    ).select_related('subject', 'teacher__profile__user').order_by('subject__name') if selected_term else []
    
    # Calculate average
    average = grades.aggregate(avg=Avg('marks_obtained'))['avg'] if grades else 0
    
    context = {
        'student': student,
        'grades': grades,
        'terms': terms,
        'selected_term': selected_term,
        'average': round(average, 2) if average else 0,
    }
    
    return render(request, 'portal/student/grades.html', context)

@login_required
@user_passes_test(is_student, login_url='portal:login')
def student_assignments(request):
    """Student assignments view"""
    student = get_object_or_404(Student, profile__user=request.user)
    
    # Get assignments for student's class
    assignments = Assignment.objects.filter(
        class_obj=student.current_class,
        status='published'
    ).select_related('subject', 'teacher__profile__user').order_by('-due_date')
    
    # Filter by status if requested
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'pending':
        submitted_assignment_ids = AssignmentSubmission.objects.filter(
            student=student,
            status__in=['submitted', 'graded', 'returned']
        ).values_list('assignment_id', flat=True)
        assignments = assignments.exclude(id__in=submitted_assignment_ids)
    elif status_filter == 'submitted':
        submitted_assignment_ids = AssignmentSubmission.objects.filter(
            student=student,
            status__in=['submitted', 'graded', 'returned']
        ).values_list('assignment_id', flat=True)
        assignments = assignments.filter(id__in=submitted_assignment_ids)
    
    # Pagination
    paginator = Paginator(assignments, 10)
    page = request.GET.get('page')
    assignments = paginator.get_page(page)
    
    # Get submission status for each assignment
    for assignment in assignments:
        try:
            submission = AssignmentSubmission.objects.get(
                assignment=assignment,
                student=student
            )
            assignment.submission_status = submission.status
            assignment.submission = submission
        except AssignmentSubmission.DoesNotExist:
            assignment.submission_status = 'not_submitted'
            assignment.submission = None
    
    context = {
        'student': student,
        'assignments': assignments,
        'status_filter': status_filter,
    }
    
    return render(request, 'portal/student/assignments.html', context)

@login_required
@user_passes_test(is_student, login_url='portal:login')
def assignment_detail(request, assignment_id):
    """Assignment detail view"""
    student = get_object_or_404(Student, profile__user=request.user)
    assignment = get_object_or_404(Assignment, id=assignment_id, class_obj=student.current_class)
    
    try:
        submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)
    except AssignmentSubmission.DoesNotExist:
        submission = None
    
    context = {
        'student': student,
        'assignment': assignment,
        'submission': submission,
    }
    
    return render(request, 'portal/student/assignment_detail.html', context)

@login_required
@user_passes_test(is_student, login_url='portal:login')
def submit_assignment(request, assignment_id):
    """Submit assignment view"""
    student = get_object_or_404(Student, profile__user=request.user)
    assignment = get_object_or_404(Assignment, id=assignment_id, class_obj=student.current_class)
    
    # Check if assignment is still open
    if assignment.status == 'closed' or timezone.now() > assignment.due_date:
        messages.error(request, 'This assignment is no longer accepting submissions.')
        return redirect('portal:assignment_detail', assignment_id=assignment_id)
    
    try:
        submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)
        if submission.status in ['submitted', 'graded', 'returned']:
            messages.error(request, 'You have already submitted this assignment.')
            return redirect('portal:assignment_detail', assignment_id=assignment_id)
    except AssignmentSubmission.DoesNotExist:
        submission = AssignmentSubmission(assignment=assignment, student=student)
    
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = student
            submission.status = 'submitted'
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('portal:assignment_detail', assignment_id=assignment_id)
    else:
        form = AssignmentSubmissionForm(instance=submission)
    
    context = {
        'student': student,
        'assignment': assignment,
        'submission': submission,
        'form': form,
    }
    
    return render(request, 'portal/student/submit_assignment.html', context)

@login_required
@user_passes_test(is_student, login_url='portal:login')
def student_attendance(request):
    """Student attendance view"""
    student = get_object_or_404(Student, profile__user=request.user)
    
    # Get date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)  # Last 30 days by default
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    # Get attendance records
    attendance_records = Attendance.objects.filter(
        student=student,
        date__range=[start_date, end_date]
    ).order_by('-date')
    
    # Calculate statistics
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='present').count()
    absent_days = attendance_records.filter(status='absent').count()
    late_days = attendance_records.filter(status='late').count()
    excused_days = attendance_records.filter(status='excused').count()
    
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'start_date': start_date,
        'end_date': end_date,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'late_days': late_days,
        'excused_days': excused_days,
        'attendance_percentage': round(attendance_percentage, 2),
    }
    
    return render(request, 'portal/student/attendance.html', context)

@login_required
@user_passes_test(is_student, login_url='portal:login')
def progress_report(request, term_id):
    """Student progress report view"""
    student = get_object_or_404(Student, profile__user=request.user)
    term = get_object_or_404(Term, id=term_id)
    
    try:
        report = ProgressReport.objects.get(student=student, term=term)
    except ProgressReport.DoesNotExist:
        messages.error(request, 'Progress report not available for this term.')
        return redirect('portal:student_grades')
    
    # Get detailed grades for the term
    grades = Grade.objects.filter(
        student=student,
        term=term
    ).select_related('subject', 'teacher__profile__user').order_by('subject__name')
    
    context = {
        'student': student,
        'term': term,
        'report': report,
        'grades': grades,
    }
    
    return render(request, 'portal/student/progress_report.html', context)

# Parent views
@login_required
@user_passes_test(is_parent, login_url='portal:login')
def parent_dashboard(request):
    """Parent dashboard"""
    try:
        parent = Parent.objects.get(profile__user=request.user)
    except Parent.DoesNotExist:
        messages.error(request, 'Parent profile not found.')
        return redirect('portal:logout')
    
    children = parent.children.filter(is_active=True)
    current_term = get_current_term()
    
    # Get summary data for each child
    for child in children:
        # Recent grades
        child.recent_grades = Grade.objects.filter(
            student=child,
            term=current_term
        ).order_by('-date_recorded')[:3] if current_term else []
        
        # Attendance summary
        if current_term:
            attendance_data = Attendance.objects.filter(
                student=child,
                date__range=[current_term.start_date, current_term.end_date]
            ).values('status').annotate(count=Count('id'))
            child.attendance_summary = {item['status']: item['count'] for item in attendance_data}
        else:
            child.attendance_summary = {}
        
        # Pending assignments
        submitted_assignment_ids = AssignmentSubmission.objects.filter(
            student=child,
            status__in=['submitted', 'graded', 'returned']
        ).values_list('assignment_id', flat=True)
        child.pending_assignments = Assignment.objects.filter(
            class_obj=child.current_class,
            status='published',
            due_date__gte=timezone.now()
        ).exclude(id__in=submitted_assignment_ids).count()
    
    context = {
        'parent': parent,
        'children': children,
        'current_term': current_term,
    }
    
    return render(request, 'portal/parent/dashboard.html', context)

@login_required
@user_passes_test(is_parent, login_url='portal:login')
def child_profile(request, student_id):
    """Child profile view for parents"""
    parent = get_object_or_404(Parent, profile__user=request.user)
    student = get_object_or_404(Student, id=student_id)
    
    # Ensure parent can access this child
    if student not in parent.children.all():
        return HttpResponseForbidden("You don't have access to this student's information.")
    
    context = {
        'parent': parent,
        'student': student,
    }
    
    return render(request, 'portal/parent/child_profile.html', context)

@login_required
@user_passes_test(is_parent, login_url='portal:login')
def child_grades(request, student_id):
    """Child grades view for parents"""
    parent = get_object_or_404(Parent, profile__user=request.user)
    student = get_object_or_404(Student, id=student_id)
    
    # Ensure parent can access this child
    if student not in parent.children.all():
        return HttpResponseForbidden("You don't have access to this student's information.")
    
    current_term = get_current_term()
    current_year = get_current_academic_year()
    terms = Term.objects.filter(academic_year=current_year) if current_year else []
    
    selected_term_id = request.GET.get('term', current_term.id if current_term else None)
    selected_term = get_object_or_404(Term, id=selected_term_id) if selected_term_id else current_term
    
    grades = Grade.objects.filter(
        student=student,
        term=selected_term
    ).select_related('subject', 'teacher__profile__user').order_by('subject__name') if selected_term else []
    
    average = grades.aggregate(avg=Avg('marks_obtained'))['avg'] if grades else 0
    
    context = {
        'parent': parent,
        'student': student,
        'grades': grades,
        'terms': terms,
        'selected_term': selected_term,
        'average': round(average, 2) if average else 0,
    }
    
    return render(request, 'portal/parent/child_grades.html', context)

@login_required
@user_passes_test(is_parent, login_url='portal:login')
def child_attendance(request, student_id):
    """Child attendance view for parents"""
    parent = get_object_or_404(Parent, profile__user=request.user)
    student = get_object_or_404(Student, id=student_id)
    
    # Ensure parent can access this child
    if student not in parent.children.all():
        return HttpResponseForbidden("You don't have access to this student's information.")
    
    # Get date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    attendance_records = Attendance.objects.filter(
        student=student,
        date__range=[start_date, end_date]
    ).order_by('-date')
    
    # Calculate statistics
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='present').count()
    absent_days = attendance_records.filter(status='absent').count()
    late_days = attendance_records.filter(status='late').count()
    excused_days = attendance_records.filter(status='excused').count()
    
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    context = {
        'parent': parent,
        'student': student,
        'attendance_records': attendance_records,
        'start_date': start_date,
        'end_date': end_date,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'late_days': late_days,
        'excused_days': excused_days,
        'attendance_percentage': round(attendance_percentage, 2),
    }
    
    return render(request, 'portal/parent/child_attendance.html', context)

@login_required
@user_passes_test(is_parent, login_url='portal:login')
def child_report(request, student_id, term_id):
    """Child progress report view for parents"""
    parent = get_object_or_404(Parent, profile__user=request.user)
    student = get_object_or_404(Student, id=student_id)
    term = get_object_or_404(Term, id=term_id)
    
    # Ensure parent can access this child
    if student not in parent.children.all():
        return HttpResponseForbidden("You don't have access to this student's information.")
    
    try:
        report = ProgressReport.objects.get(student=student, term=term)
    except ProgressReport.DoesNotExist:
        messages.error(request, 'Progress report not available for this term.')
        return redirect('portal:child_grades', student_id=student_id)
    
    grades = Grade.objects.filter(
        student=student,
        term=term
    ).select_related('subject', 'teacher__profile__user').order_by('subject__name')
    
    context = {
        'parent': parent,
        'student': student,
        'term': term,
        'report': report,
        'grades': grades,
    }
    
    return render(request, 'portal/parent/child_report.html', context)

# Teacher views (basic structure - can be expanded)
@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def teacher_dashboard(request):
    """Teacher dashboard"""
    try:
        teacher = Teacher.objects.get(profile__user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('portal:logout')
    
    current_term = get_current_term()
    
    # Get teacher's classes
    classes = Class.objects.filter(class_teacher=teacher)
    
    # Get recent assignments
    recent_assignments = Assignment.objects.filter(
        teacher=teacher,
        created_at__gte=timezone.now() - timedelta(days=30)
    ).order_by('-created_at')[:5]
    
    # Get pending submissions to grade
    pending_submissions = AssignmentSubmission.objects.filter(
        assignment__teacher=teacher,
        status='submitted'
    ).count()
    
    context = {
        'teacher': teacher,
        'classes': classes,
        'current_term': current_term,
        'recent_assignments': recent_assignments,
        'pending_submissions': pending_submissions,
    }
    
    return render(request, 'portal/teacher/dashboard.html', context)

# Additional teacher views would go here...
# (create_assignment, teacher_assignments, assignment_submissions, etc.)

# Communication views
@login_required
def messages_inbox(request):
    """Messages inbox"""
    messages_list = Communication.objects.filter(
        recipients=request.user
    ).order_by('-created_at')
    
    paginator = Paginator(messages_list, 20)
    page = request.GET.get('page')
    messages_list = paginator.get_page(page)
    
    context = {
        'messages': messages_list,
    }
    
    return render(request, 'portal/messages/inbox.html', context)

@login_required
def message_detail(request, message_id):
    """Message detail view"""
    message = get_object_or_404(Communication, id=message_id)
    
    # Check if user is recipient
    if request.user not in message.recipients.all():
        return HttpResponseForbidden("You don't have access to this message.")
    
    # Mark as read
    message.read_by.add(request.user)
    
    context = {
        'message': message,
    }
    
    return render(request, 'portal/messages/detail.html', context)

# API endpoints
@login_required
def api_student_data(request, student_id):
    """API endpoint for student data"""
    # Check permissions
    if is_student(request.user):
        student = get_object_or_404(Student, profile__user=request.user)
        if student.id != student_id:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    elif is_parent(request.user):
        parent = get_object_or_404(Parent, profile__user=request.user)
        student = get_object_or_404(Student, id=student_id)
        if student not in parent.children.all():
            return JsonResponse({'error': 'Permission denied'}, status=403)
    elif is_teacher(request.user):
        teacher = get_object_or_404(Teacher, profile__user=request.user)
        student = get_object_or_404(Student, id=student_id)
        # Check if teacher teaches this student's class
        if student.current_class not in Class.objects.filter(class_teacher=teacher):
            return JsonResponse({'error': 'Permission denied'}, status=403)
    else:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    student = get_object_or_404(Student, id=student_id)
    data = {
        'name': student.full_name,
        'admission_number': student.admission_number,
        'class': student.current_class.display_name if student.current_class else '',
        'gender': student.get_gender_display(),
        'age': student.age,
    }
    
    return JsonResponse(data)

# Admin dashboard (basic)
@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    if not request.user.is_staff:
        return HttpResponseForbidden("Access denied.")
    
    # Get summary statistics
    total_students = Student.objects.filter(is_active=True).count()
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_classes = Class.objects.count()
    current_term = get_current_term()
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'current_term': current_term,
    }
    
    return render(request, 'portal/admin/dashboard.html', context)

# Placeholder views for remaining teacher functions
@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def teacher_classes(request):
    """Teacher classes view - placeholder"""
    return render(request, 'portal/teacher/classes.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def class_detail(request, class_id):
    """Class detail view - placeholder"""
    return render(request, 'portal/teacher/class_detail.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def teacher_assignments(request):
    """Teacher assignments view - placeholder"""
    return render(request, 'portal/teacher/assignments.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def create_assignment(request):
    """Create assignment view - placeholder"""
    return render(request, 'portal/teacher/create_assignment.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def assignment_submissions(request, assignment_id):
    """Assignment submissions view - placeholder"""
    return render(request, 'portal/teacher/assignment_submissions.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def grade_submission(request, submission_id):
    """Grade submission view - placeholder"""
    return render(request, 'portal/teacher/grade_submission.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def teacher_grades(request):
    """Teacher grades view - placeholder"""
    return render(request, 'portal/teacher/grades.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def add_grade(request):
    """Add grade view - placeholder"""
    return render(request, 'portal/teacher/add_grade.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def teacher_attendance(request):
    """Teacher attendance view - placeholder"""
    return render(request, 'portal/teacher/attendance.html', {})

@login_required
@user_passes_test(is_teacher, login_url='portal:login')
def mark_attendance(request, class_id):
    """Mark attendance view - placeholder"""
    return render(request, 'portal/teacher/mark_attendance.html', {})

@login_required
def compose_message(request):
    """Compose message view - placeholder"""
    return render(request, 'portal/messages/compose.html', {})

@login_required
def api_attendance_summary(request, student_id):
    """API endpoint for attendance summary - placeholder"""
    return JsonResponse({'status': 'placeholder'})

@login_required
def api_grade_summary(request, student_id):
    """API endpoint for grade summary - placeholder"""
    return JsonResponse({'status': 'placeholder'})