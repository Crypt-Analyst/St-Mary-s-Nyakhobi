from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    # Main portal dashboard
    path('', views.portal_dashboard, name='dashboard'),
    
    # Authentication
    path('login/', views.portal_login, name='login'),
    path('logout/', views.portal_logout, name='logout'),
    
    # Student views
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/grades/', views.student_grades, name='student_grades'),
    path('student/assignments/', views.student_assignments, name='student_assignments'),
    path('student/assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('student/assignments/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('student/attendance/', views.student_attendance, name='student_attendance'),
    path('student/report/<int:term_id>/', views.progress_report, name='progress_report'),
    
    # Parent views
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/child/<int:student_id>/', views.child_profile, name='child_profile'),
    path('parent/child/<int:student_id>/grades/', views.child_grades, name='child_grades'),
    path('parent/child/<int:student_id>/attendance/', views.child_attendance, name='child_attendance'),
    path('parent/child/<int:student_id>/report/<int:term_id>/', views.child_report, name='child_report'),
    
    # Teacher views
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/classes/', views.teacher_classes, name='teacher_classes'),
    path('teacher/class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('teacher/assignments/', views.teacher_assignments, name='teacher_assignments'),
    path('teacher/assignments/create/', views.create_assignment, name='create_assignment'),
    path('teacher/assignments/<int:assignment_id>/submissions/', views.assignment_submissions, name='assignment_submissions'),
    path('teacher/assignments/submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('teacher/grades/', views.teacher_grades, name='teacher_grades'),
    path('teacher/grades/add/', views.add_grade, name='add_grade'),
    path('teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('teacher/attendance/<int:class_id>/', views.mark_attendance, name='mark_attendance'),
    
    # Communication
    path('messages/', views.messages_inbox, name='messages_inbox'),
    path('messages/compose/', views.compose_message, name='compose_message'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    
    # API endpoints for AJAX requests
    path('api/student-data/<int:student_id>/', views.api_student_data, name='api_student_data'),
    path('api/attendance-summary/<int:student_id>/', views.api_attendance_summary, name='api_attendance_summary'),
    path('api/grade-summary/<int:student_id>/', views.api_grade_summary, name='api_grade_summary'),
]