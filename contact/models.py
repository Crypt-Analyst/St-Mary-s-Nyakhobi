from django.db import models
from django.utils import timezone

class ContactInquiry(models.Model):
    """Contact form submissions"""
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('admission', 'Admission Information'),
        ('academic', 'Academic Question'),
        ('complaint', 'Complaint/Feedback'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_replied = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Contact Inquiries"