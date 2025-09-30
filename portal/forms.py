from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import models
from .models import (
    UserProfile, Assignment, AssignmentSubmission, Grade, Attendance,
    Communication, Student, Teacher, Parent, Class, Subject, Term
)

class LoginForm(forms.Form):
    """Login form for the portal"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            # Try to authenticate with username first, then email
            user = authenticate(username=username, password=password)
            if not user:
                # Try with email
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if not user:
                raise forms.ValidationError('Invalid username/email or password.')
            elif not user.is_active:
                raise forms.ValidationError('This account is inactive.')
        
        return cleaned_data

class ProfileForm(forms.ModelForm):
    """User profile form"""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth', 'profile_picture', 
                 'emergency_contact', 'emergency_phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update user fields
            profile.user.first_name = self.cleaned_data.get('first_name', '')
            profile.user.last_name = self.cleaned_data.get('last_name', '')
            profile.user.email = self.cleaned_data.get('email', '')
            profile.user.save()
            profile.save()
        return profile

class AssignmentForm(forms.ModelForm):
    """Form for creating/editing assignments"""
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'subject', 'class_obj', 'assignment_type',
                 'due_date', 'max_marks', 'instructions', 'attachments', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'class_obj': forms.Select(attrs={'class': 'form-select'}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'attachments': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            # Limit subjects to those taught by the teacher
            self.fields['subject'].queryset = teacher.subjects.all()
            
            # Limit classes to those taught by the teacher
            self.fields['class_obj'].queryset = Class.objects.filter(
                models.Q(class_teacher=teacher) |
                models.Q(class_subjects__teacher=teacher)
            ).distinct()

class AssignmentSubmissionForm(forms.ModelForm):
    """Form for assignment submissions"""
    class Meta:
        model = AssignmentSubmission
        fields = ['submission_text', 'attachment']
        widgets = {
            'submission_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Enter your submission text here...'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt,.jpg,.jpeg,.png'
            }),
        }

class GradeForm(forms.ModelForm):
    """Form for adding/editing grades"""
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'term', 'grade_type', 'title',
                 'marks_obtained', 'max_marks', 'weight', 'comments']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'term': forms.Select(attrs={'class': 'form-select'}),
            'grade_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'max_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '1'
            }),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        class_obj = kwargs.pop('class_obj', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            self.fields['subject'].queryset = teacher.subjects.all()
        
        if class_obj:
            self.fields['student'].queryset = Student.objects.filter(
                current_class=class_obj,
                is_active=True
            )

class AttendanceForm(forms.ModelForm):
    """Form for marking attendance"""
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'time_in', 'time_out', 'notes']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'time_in': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'time_out': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class BulkAttendanceForm(forms.Form):
    """Form for bulk attendance marking"""
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    class_obj = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Class'
    )
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            self.fields['class_obj'].queryset = Class.objects.filter(
                models.Q(class_teacher=teacher) |
                models.Q(class_subjects__teacher=teacher)
            ).distinct()

class MessageForm(forms.ModelForm):
    """Form for composing messages"""
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Communication
        fields = ['recipients', 'message_type', 'priority', 'subject', 'message', 'attachment']
        widgets = {
            'message_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)
        
        # Filter recipients based on user type
        if user_type == 'teacher':
            # Teachers can message students, parents, and other teachers
            self.fields['recipients'].queryset = User.objects.filter(
                userprofile__user_type__in=['student', 'parent', 'teacher']
            ).exclude(is_active=False)
        elif user_type == 'parent':
            # Parents can message teachers and admin
            self.fields['recipients'].queryset = User.objects.filter(
                userprofile__user_type__in=['teacher', 'admin']
            ).exclude(is_active=False)
        elif user_type == 'student':
            # Students can message teachers
            self.fields['recipients'].queryset = User.objects.filter(
                userprofile__user_type='teacher'
            ).exclude(is_active=False)
        else:
            # Admin can message everyone
            self.fields['recipients'].queryset = User.objects.filter(
                is_active=True
            )

class StudentSearchForm(forms.Form):
    """Form for searching students"""
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name or admission number...'
        })
    )
    class_filter = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        required=False,
        empty_label='All Classes',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    gender_filter = forms.ChoiceField(
        choices=[('', 'All Genders')] + Student.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status_filter = forms.ChoiceField(
        choices=[
            ('', 'All Students'),
            ('active', 'Active Students'),
            ('inactive', 'Inactive Students')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class TeacherSearchForm(forms.Form):
    """Form for searching teachers"""
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name or employee ID...'
        })
    )
    subject_filter = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label='All Subjects',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    employment_status_filter = forms.ChoiceField(
        choices=[('', 'All Status')] + Teacher.EMPLOYMENT_STATUS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class AssignmentFilterForm(forms.Form):
    """Form for filtering assignments"""
    subject_filter = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label='All Subjects',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class_filter = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        required=False,
        empty_label='All Classes',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    type_filter = forms.ChoiceField(
        choices=[('', 'All Types')] + Assignment.ASSIGNMENT_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status_filter = forms.ChoiceField(
        choices=[('', 'All Status')] + Assignment.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

class GradeFilterForm(forms.Form):
    """Form for filtering grades"""
    student_filter = forms.ModelChoiceField(
        queryset=Student.objects.filter(is_active=True),
        required=False,
        empty_label='All Students',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject_filter = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label='All Subjects',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    term_filter = forms.ModelChoiceField(
        queryset=Term.objects.all(),
        required=False,
        empty_label='All Terms',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    grade_type_filter = forms.ChoiceField(
        choices=[('', 'All Types')] + Grade.GRADE_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class DateRangeForm(forms.Form):
    """Form for date range selection"""
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('Start date cannot be after end date.')
        
        return cleaned_data

class QuickMessageForm(forms.Form):
    """Form for quick messages"""
    MESSAGE_TYPES = [
        ('absence', 'Report Absence'),
        ('pickup', 'Early Pickup'),
        ('medical', 'Medical Issue'),
        ('general', 'General Inquiry'),
    ]
    
    message_type = forms.ChoiceField(
        choices=MESSAGE_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message...'
        })
    )
    urgent = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )