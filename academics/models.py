from django.db import models

class GradeLevel(models.Model):
    """Grade levels offered by the school"""
    name = models.CharField(max_length=50)  # e.g., "Grade 1", "Kindergarten"
    description = models.TextField(blank=True)
    age_range = models.CharField(max_length=50, blank=True)  # e.g., "5-6 years"
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Subject(models.Model):
    """Academic subjects"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    grade_levels = models.ManyToManyField(GradeLevel)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class AcademicProgram(models.Model):
    """Academic programs offered"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    grade_levels = models.ManyToManyField(GradeLevel)
    subjects = models.ManyToManyField(Subject, blank=True)
    duration = models.CharField(max_length=100, blank=True)  # e.g., "4 years"
    requirements = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class AcademicCalendar(models.Model):
    """Academic calendar events"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_holiday = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['start_date']