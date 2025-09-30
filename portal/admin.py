from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg
from .models import (
    AcademicYear, Class, Subject, ClassSubject, UserProfile, Teacher, Student,
    Parent, Term, Assignment, AssignmentSubmission, Grade, Attendance,
    ProgressReport, Communication, PortalSettings
)

# Unregister the default User admin
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('user_type', 'phone', 'address', 'date_of_birth', 'profile_picture', 
              'emergency_contact', 'emergency_phone')

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_user_type', 'is_staff', 'date_joined')
    list_filter = BaseUserAdmin.list_filter + ('userprofile__user_type',)
    
    def get_user_type(self, obj):
        try:
            return obj.userprofile.get_user_type_display()
        except UserProfile.DoesNotExist:
            return "No Profile"
    get_user_type.short_description = 'User Type'
    get_user_type.admin_order_field = 'userprofile__user_type'

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current', 'get_classes_count')
    list_filter = ('is_current', 'start_date')
    search_fields = ('name',)
    date_hierarchy = 'start_date'
    
    def get_classes_count(self, obj):
        return obj.class_set.count()
    get_classes_count.short_description = 'Classes'

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'academic_year', 'class_teacher', 'get_student_count', 'capacity', 'level')
    list_filter = ('academic_year', 'level', 'name')
    search_fields = ('name', 'display_name', 'class_teacher__profile__user__first_name', 
                    'class_teacher__profile__user__last_name')
    ordering = ('academic_year', 'level')
    
    def get_student_count(self, obj):
        count = obj.student_count
        if count > obj.capacity:
            return format_html('<span style="color: red;">{}/{}</span>', count, obj.capacity)
        return f"{count}/{obj.capacity}"
    get_student_count.short_description = 'Enrollment'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_core', 'get_classes_count')
    list_filter = ('is_core',)
    search_fields = ('name', 'code')
    filter_horizontal = ('classes',)
    
    def get_classes_count(self, obj):
        return obj.classes.count()
    get_classes_count.short_description = 'Classes'

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'subject', 'teacher', 'lessons_per_week')
    list_filter = ('class_obj__academic_year', 'subject__is_core')
    search_fields = ('class_obj__name', 'subject__name', 'teacher__profile__user__first_name')
    raw_id_fields = ('teacher',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'employee_id', 'employment_status', 'hire_date', 
                   'get_subjects_count', 'get_classes_count', 'is_active')
    list_filter = ('employment_status', 'is_active', 'hire_date', 'subjects')
    search_fields = ('profile__user__first_name', 'profile__user__last_name', 'employee_id')
    filter_horizontal = ('subjects',)
    date_hierarchy = 'hire_date'
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Full Name'
    
    def get_subjects_count(self, obj):
        return obj.subjects.count()
    get_subjects_count.short_description = 'Subjects'
    
    def get_classes_count(self, obj):
        return obj.class_set.count()
    get_classes_count.short_description = 'Classes'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'admission_number', 'current_class', 'gender', 
                   'admission_date', 'get_age', 'parent_guardian', 'is_active')
    list_filter = ('current_class', 'gender', 'is_active', 'admission_date')
    search_fields = ('profile__user__first_name', 'profile__user__last_name', 'admission_number')
    date_hierarchy = 'admission_date'
    raw_id_fields = ('parent_guardian',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('profile', 'admission_number', 'current_class', 'gender')
        }),
        ('Academic Information', {
            'fields': ('admission_date', 'graduation_year', 'previous_school')
        }),
        ('Family Information', {
            'fields': ('parent_guardian',)
        }),
        ('Health Information', {
            'fields': ('medical_conditions',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Full Name'
    
    def get_age(self, obj):
        return obj.age
    get_age.short_description = 'Age'

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'relationship', 'occupation', 'is_primary_contact', 
                   'get_children_count')
    list_filter = ('relationship', 'is_primary_contact')
    search_fields = ('profile__user__first_name', 'profile__user__last_name', 'occupation')
    filter_horizontal = ('children',)
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Full Name'
    
    def get_children_count(self, obj):
        return obj.children.count()
    get_children_count.short_description = 'Children'

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'term_number', 'start_date', 'end_date', 'is_current')
    list_filter = ('academic_year', 'term_number', 'is_current')
    date_hierarchy = 'start_date'
    ordering = ('-academic_year', 'term_number')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'class_obj', 'teacher', 'assignment_type', 
                   'due_date', 'max_marks', 'get_submission_count', 'status', 'is_overdue')
    list_filter = ('assignment_type', 'status', 'subject', 'class_obj', 'due_date')
    search_fields = ('title', 'description', 'teacher__profile__user__first_name')
    date_hierarchy = 'due_date'
    raw_id_fields = ('teacher',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'subject', 'class_obj', 'teacher')
        }),
        ('Assignment Details', {
            'fields': ('assignment_type', 'due_date', 'max_marks', 'instructions')
        }),
        ('Attachments & Status', {
            'fields': ('attachments', 'status')
        })
    )
    
    def get_submission_count(self, obj):
        return obj.submission_count
    get_submission_count.short_description = 'Submissions'
    
    def is_overdue(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">Yes</span>')
        return 'No'
    is_overdue.short_description = 'Overdue'
    is_overdue.boolean = True

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'submitted_at', 'marks_obtained', 
                   'get_percentage_score', 'is_late')
    list_filter = ('status', 'is_late', 'submitted_at', 'assignment__subject')
    search_fields = ('student__profile__user__first_name', 'student__profile__user__last_name',
                    'assignment__title')
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Submission Information', {
            'fields': ('assignment', 'student', 'status')
        }),
        ('Content', {
            'fields': ('submission_text', 'attachment')
        }),
        ('Grading', {
            'fields': ('marks_obtained', 'teacher_feedback')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'is_late'),
            'classes': ('collapse',)
        })
    )
    
    def get_percentage_score(self, obj):
        score = obj.percentage_score
        if score is not None:
            if score >= 70:
                return format_html('<span style="color: green;">{:.1f}%</span>', score)
            elif score >= 50:
                return format_html('<span style="color: orange;">{:.1f}%</span>', score)
            else:
                return format_html('<span style="color: red;">{:.1f}%</span>', score)
        return 'Not Graded'
    get_percentage_score.short_description = 'Score %'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'grade_type', 'title', 
                   'marks_obtained', 'max_marks', 'get_percentage_score', 'get_letter_grade')
    list_filter = ('grade_type', 'subject', 'term', 'date_recorded')
    search_fields = ('student__profile__user__first_name', 'student__profile__user__last_name',
                    'title')
    date_hierarchy = 'date_recorded'
    
    def get_percentage_score(self, obj):
        score = obj.percentage_score
        if score >= 90:
            color = 'green'
        elif score >= 80:
            color = 'blue'
        elif score >= 70:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{:.1f}%</span>', color, score)
    get_percentage_score.short_description = 'Score %'
    
    def get_letter_grade(self, obj):
        grade = obj.letter_grade
        colors = {'A': 'green', 'B': 'blue', 'C': 'orange', 'D': 'darkorange', 'E': 'red'}
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 
                          colors.get(grade, 'black'), grade)
    get_letter_grade.short_description = 'Grade'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'time_in', 'time_out', 'marked_by')
    list_filter = ('status', 'date', 'student__current_class')
    search_fields = ('student__profile__user__first_name', 'student__profile__user__last_name')
    date_hierarchy = 'date'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student__profile__user', 'marked_by__profile__user')

@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'overall_average', 'class_position', 'total_students',
                   'conduct_grade', 'effort_grade', 'generated_at')
    list_filter = ('term', 'conduct_grade', 'effort_grade')
    search_fields = ('student__profile__user__first_name', 'student__profile__user__last_name')
    date_hierarchy = 'generated_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'term', 'class_teacher')
        }),
        ('Academic Performance', {
            'fields': ('overall_average', 'class_position', 'total_students')
        }),
        ('Behavior Assessment', {
            'fields': ('conduct_grade', 'effort_grade')
        }),
        ('Comments', {
            'fields': ('teacher_comments', 'principal_comments', 'parent_comments')
        }),
        ('Next Term', {
            'fields': ('next_term_begins',)
        })
    )

@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'message_type', 'priority', 'get_recipients_count',
                   'get_unread_count', 'is_broadcast', 'created_at')
    list_filter = ('message_type', 'priority', 'is_broadcast', 'created_at')
    search_fields = ('subject', 'message', 'sender__first_name', 'sender__last_name')
    filter_horizontal = ('recipients', 'read_by')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('sender', 'message_type', 'priority', 'subject', 'message')
        }),
        ('Recipients', {
            'fields': ('recipients', 'is_broadcast')
        }),
        ('Attachments', {
            'fields': ('attachment',)
        }),
        ('Read Status', {
            'fields': ('read_by',),
            'classes': ('collapse',)
        })
    )
    
    def get_recipients_count(self, obj):
        return obj.recipients.count()
    get_recipients_count.short_description = 'Recipients'
    
    def get_unread_count(self, obj):
        unread = obj.unread_count
        if unread > 0:
            return format_html('<span style="color: red;">{}</span>', unread)
        return unread
    get_unread_count.short_description = 'Unread'

@admin.register(PortalSettings)
class PortalSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'attendance_required', 'parent_access_enabled', 
                   'assignment_submission_enabled', 'updated_at')
    
    fieldsets = (
        ('Academic Settings', {
            'fields': ('school_year_start_month', 'grading_scale')
        }),
        ('Feature Settings', {
            'fields': ('attendance_required', 'parent_access_enabled', 
                      'assignment_submission_enabled', 'communication_enabled',
                      'report_generation_enabled')
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not PortalSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

# Register the modified User admin
admin.site.register(User, UserAdmin)

# Customize admin site
admin.site.site_header = "St. Mary's Nyakhobi School - Student Portal Administration"
admin.site.site_title = "Student Portal Admin"
admin.site.index_title = "Welcome to Student Portal Administration"