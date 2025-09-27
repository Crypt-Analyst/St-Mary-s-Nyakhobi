from django.db import models
from django.utils import timezone
from django.urls import reverse

class Event(models.Model):
    """School events"""
    EVENT_TYPES = [
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('exam', 'Examination'),
        ('holiday', 'Holiday'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    image = models.ImageField(upload_to='events/', blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-event_date']

class News(models.Model):
    """School news and announcements"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.CharField(max_length=300, help_text="Brief summary for listings")
    image = models.ImageField(upload_to='news/', blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "News"
        ordering = ['-created_at']

class Gallery(models.Model):
    """Photo gallery"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ['-uploaded_at']