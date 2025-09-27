from django.db import models

class Department(models.Model):
    """School departments"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    head_of_department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Faculty(models.Model):
    """Faculty and staff members"""
    POSITION_CHOICES = [
        ('principal', 'Principal'),
        ('vice_principal', 'Vice Principal'),
        ('teacher', 'Teacher'),
        ('admin_staff', 'Administrative Staff'),
        ('support_staff', 'Support Staff'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True, help_text="Brief biography")
    qualifications = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='faculty/', blank=True)
    subjects_taught = models.CharField(max_length=200, blank=True, help_text="Comma-separated subjects")
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name_plural = "Faculty"
        ordering = ['position', 'last_name']