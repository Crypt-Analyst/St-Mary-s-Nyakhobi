from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
import uuid

class AcademicYear(models.Model):
    """Academic year model"""
    name = models.CharField(max_length=50, unique=True, help_text="e.g., 2024-2025")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_current:
            # Ensure only one academic year is current
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

class Class(models.Model):
    """Class/Grade model"""
    CLASS_LEVELS = [
        ('PP1', 'Pre-Primary 1'),
        ('PP2', 'Pre-Primary 2'),
        ('Grade1', 'Grade 1'),
        ('Grade2', 'Grade 2'), 
        ('Grade3', 'Grade 3'),
        ('Grade4', 'Grade 4'),
        ('Grade5', 'Grade 5'),
        ('Grade6', 'Grade 6'),
        ('Grade7', 'Grade 7'),
        ('Grade8', 'Grade 8'),
        ('Form1', 'Form 1'),
        ('Form2', 'Form 2'),
        ('Form3', 'Form 3'),
        ('Form4', 'Form 4'),
    ]
    
    name = models.CharField(max_length=20, choices=CLASS_LEVELS, unique=True)
    display_name = models.CharField(max_length=50)
    level = models.IntegerField(help_text="Numeric level for ordering (1-14)")
    capacity = models.PositiveIntegerField(default=40)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['level']
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        unique_together = ['name', 'academic_year']
    
    def __str__(self):
        return f"{self.display_name} ({self.academic_year})"
    
    @property
    def student_count(self):
        return self.students.count()

class Subject(models.Model):
    """Subject model"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_core = models.BooleanField(default=True, help_text="Is this a core/compulsory subject?")
    classes = models.ManyToManyField(Class, through='ClassSubject')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class ClassSubject(models.Model):
    """Through model for Class and Subject relationship"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_classes')
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    lessons_per_week = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['class_obj', 'subject']
        verbose_name = "Class Subject"
        verbose_name_plural = "Class Subjects"
    
    def __str__(self):
        return f"{self.class_obj.display_name} - {self.subject.name}"

class UserProfile(models.Model):
    """Base profile for extending Django User"""
    USER_TYPES = [
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_user_type_display()})"

class Teacher(models.Model):
    """Teacher model"""
    EMPLOYMENT_STATUS = [
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('intern', 'Intern'),
    ]
    
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, default='permanent')
    hire_date = models.DateField()
    qualifications = models.TextField(help_text="Educational qualifications and certifications")
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['profile__user__first_name', 'profile__user__last_name']
    
    def __str__(self):
        return f"Teacher {self.profile.user.get_full_name()}"
    
    @property
    def full_name(self):
        return self.profile.user.get_full_name()

class Student(models.Model):
    """Student model"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=20, unique=True)
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    admission_date = models.DateField()
    parent_guardian = models.ForeignKey('Parent', on_delete=models.SET_NULL, null=True, blank=True)
    medical_conditions = models.TextField(blank=True, help_text="Any medical conditions or allergies")
    previous_school = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['admission_number']
    
    def __str__(self):
        return f"{self.profile.user.get_full_name()} ({self.admission_number})"
    
    @property
    def full_name(self):
        return self.profile.user.get_full_name()
    
    @property
    def age(self):
        if self.profile.date_of_birth:
            today = timezone.now().date()
            return today.year - self.profile.date_of_birth.year - (
                (today.month, today.day) < (self.profile.date_of_birth.month, self.profile.date_of_birth.day)
            )
        return None

class Parent(models.Model):
    """Parent/Guardian model"""
    RELATIONSHIP_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
        ('grandfather', 'Grandfather'),
        ('grandmother', 'Grandmother'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
        ('other', 'Other'),
    ]
    
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    occupation = models.CharField(max_length=100, blank=True)
    workplace = models.CharField(max_length=200, blank=True)
    work_phone = models.CharField(max_length=20, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    is_primary_contact = models.BooleanField(default=True)
    children = models.ManyToManyField(Student, related_name='parents', blank=True)
    
    class Meta:
        ordering = ['profile__user__first_name', 'profile__user__last_name']
    
    def __str__(self):
        return f"{self.profile.user.get_full_name()} ({self.get_relationship_display()})"
    
    @property
    def full_name(self):
        return self.profile.user.get_full_name()

class Term(models.Model):
    """Academic term model"""
    TERM_CHOICES = [
        (1, 'Term 1'),
        (2, 'Term 2'),
        (3, 'Term 3'),
    ]
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term_number = models.IntegerField(choices=TERM_CHOICES)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['academic_year', 'term_number']
        unique_together = ['academic_year', 'term_number']
    
    def __str__(self):
        return f"{self.academic_year.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if self.is_current:
            # Ensure only one term is current
            Term.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

class Assignment(models.Model):
    """Assignment model"""
    ASSIGNMENT_TYPES = [
        ('homework', 'Homework'),
        ('project', 'Project'),
        ('quiz', 'Quiz'),
        ('test', 'Test'),
        ('exam', 'Exam'),
        ('practical', 'Practical'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES, default='homework')
    due_date = models.DateTimeField()
    max_marks = models.PositiveIntegerField(default=100)
    instructions = models.TextField(blank=True)
    attachments = models.FileField(upload_to='assignments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.title} - {self.class_obj.display_name} ({self.subject.code})"
    
    @property
    def is_overdue(self):
        return timezone.now() > self.due_date and self.status != 'closed'
    
    @property
    def submission_count(self):
        return self.submissions.count()

class AssignmentSubmission(models.Model):
    """Assignment submission model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('returned', 'Returned'),
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submission_text = models.TextField(blank=True)
    attachment = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    teacher_feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_late = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.assignment.title}"
    
    @property
    def percentage_score(self):
        if self.marks_obtained and self.assignment.max_marks:
            return round((self.marks_obtained / self.assignment.max_marks) * 100, 1)
        return None
    
    def save(self, *args, **kwargs):
        if self.status == 'submitted' and not self.submitted_at:
            self.submitted_at = timezone.now()
            self.is_late = self.submitted_at > self.assignment.due_date
        super().save(*args, **kwargs)

class Grade(models.Model):
    """Grade/Mark model"""
    GRADE_TYPES = [
        ('assignment', 'Assignment'),
        ('test', 'Test'),
        ('exam', 'Exam'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
        ('participation', 'Class Participation'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPES)
    title = models.CharField(max_length=200)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.0, help_text="Weight in final grade calculation")
    comments = models.TextField(blank=True)
    date_recorded = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_recorded']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.subject.code} - {self.title}"
    
    @property
    def percentage_score(self):
        return round((self.marks_obtained / self.max_marks) * 100, 1)
    
    @property
    def letter_grade(self):
        """Convert percentage to letter grade"""
        percentage = self.percentage_score
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'E'

class Attendance(models.Model):
    """Student attendance model"""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.date} ({self.get_status_display()})"

class ProgressReport(models.Model):
    """Progress report model"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_reports')
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    overall_average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    class_position = models.PositiveIntegerField(null=True, blank=True)
    total_students = models.PositiveIntegerField(null=True, blank=True)
    conduct_grade = models.CharField(max_length=2, blank=True)
    effort_grade = models.CharField(max_length=2, blank=True)
    teacher_comments = models.TextField(blank=True)
    principal_comments = models.TextField(blank=True)
    parent_comments = models.TextField(blank=True)
    next_term_begins = models.DateField(null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'term']
        ordering = ['-term__start_date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.term}"

class Communication(models.Model):
    """Communication/Message model"""
    MESSAGE_TYPES = [
        ('announcement', 'General Announcement'),
        ('assignment', 'Assignment Update'),
        ('grade', 'Grade Notification'),
        ('attendance', 'Attendance Alert'),
        ('fee', 'Fee Reminder'),
        ('event', 'Event Notification'),
        ('disciplinary', 'Disciplinary Matter'),
        ('general', 'General Message'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipients = models.ManyToManyField(User, related_name='received_messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='general')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    attachment = models.FileField(upload_to='communications/', blank=True, null=True)
    is_broadcast = models.BooleanField(default=False)
    read_by = models.ManyToManyField(User, blank=True, related_name='read_communications')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.sender.get_full_name()}"
    
    @property
    def unread_count(self):
        return self.recipients.count() - self.read_by.count()

class PortalSettings(models.Model):
    """Portal system settings"""
    school_year_start_month = models.PositiveIntegerField(default=1, help_text="Month when school year starts (1-12)")
    grading_scale = models.JSONField(default=dict, help_text="Grading scale configuration")
    attendance_required = models.BooleanField(default=True)
    parent_access_enabled = models.BooleanField(default=True)
    assignment_submission_enabled = models.BooleanField(default=True)
    communication_enabled = models.BooleanField(default=True)
    report_generation_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Portal Settings"
        verbose_name_plural = "Portal Settings"
    
    def __str__(self):
        return "Portal Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and PortalSettings.objects.exists():
            raise ValueError("Only one PortalSettings instance is allowed")
        super().save(*args, **kwargs)