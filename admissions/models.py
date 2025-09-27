from django.db import models
from academics.models import GradeLevel

class AdmissionApplication(models.Model):
    """Student admission applications"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlist', 'Waitlisted'),
    ]
    
    # Student Information
    student_first_name = models.CharField(max_length=50)
    student_last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    
    # Parent/Guardian Information
    parent_first_name = models.CharField(max_length=50)
    parent_last_name = models.CharField(max_length=50)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Application Details
    previous_school = models.CharField(max_length=200, blank=True)
    medical_conditions = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    
    # Administrative
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.student_first_name} {self.student_last_name} - {self.grade_level}"
    
    class Meta:
        ordering = ['-application_date']

class AdmissionRequirement(models.Model):
    """Admission requirements by grade level"""
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    requirement_title = models.CharField(max_length=200)
    requirement_description = models.TextField()
    is_mandatory = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.grade_level} - {self.requirement_title}"