from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SchoolSettings(models.Model):
    """Global school settings"""
    school_name = models.CharField(max_length=200, default="St. Mary's Nyakhobi Senior School")
    school_motto = models.CharField(max_length=200, default="Sacrifice for Success")
    school_logo = models.ImageField(upload_to='settings/', null=True, blank=True)
    
    # Contact Information
    email = models.EmailField(default='nyakhobisecsch@gmail.com')
    phone = models.CharField(max_length=20, default='+254 700 000 000')
    address = models.TextField(default='Funyula, Busia County, Kenya')
    
    # Social Media Links
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    
    # About Us
    about_text = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'School Settings'
        verbose_name_plural = 'School Settings'
    
    def __str__(self):
        return self.school_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class NewsAnnouncement(models.Model):
    """News and announcements management"""
    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('announcement', 'Announcement'),
        ('event', 'Event'),
        ('achievement', 'Achievement'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='news')
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='news_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News & Announcement'
        verbose_name_plural = 'News & Announcements'
    
    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    """Gallery photos and videos management"""
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video URL'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='photo')
    
    # For photos
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    
    # For video URLs (YouTube, etc.)
    video_url = models.URLField(blank=True, null=True)
    
    category = models.CharField(max_length=100, default='General')
    featured = models.BooleanField(default=False)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Gallery Item'
        verbose_name_plural = 'Gallery Items'
    
    def __str__(self):
        return self.title


class TeacherProfile(models.Model):
    """Teacher/Staff profiles management"""
    DEPARTMENT_CHOICES = [
        ('languages', 'Languages'),
        ('sciences', 'Sciences'),
        ('mathematics', 'Mathematics'),
        ('humanities', 'Humanities'),
        ('technical', 'Technical Subjects'),
        ('admin', 'Administration'),
    ]
    
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    subjects = models.CharField(max_length=200, help_text="Comma-separated subjects")
    qualifications = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class SchoolEvent(models.Model):
    """School events and calendar management"""
    EVENT_TYPE_CHOICES = [
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('meeting', 'Meeting'),
        ('holiday', 'Holiday'),
        ('exam', 'Examination'),
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    description = models.TextField()
    
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    
    location = models.CharField(max_length=200, blank=True)
    all_day = models.BooleanField(default=False)
    
    published = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_date', 'start_time']
        verbose_name = 'School Event'
        verbose_name_plural = 'School Events'
    
    def __str__(self):
        return f"{self.title} - {self.start_date}"


class DownloadableFile(models.Model):
    """Downloads section - timetables, newsletters, circulars"""
    CATEGORY_CHOICES = [
        ('timetable', 'Timetable'),
        ('newsletter', 'Newsletter'),
        ('circular', 'Circular'),
        ('form', 'Form'),
        ('policy', 'Policy Document'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    
    file = models.FileField(upload_to='downloads/')
    file_size = models.CharField(max_length=20, blank=True)
    
    published = models.BooleanField(default=True)
    download_count = models.IntegerField(default=0)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Downloadable File'
        verbose_name_plural = 'Downloadable Files'
    
    def __str__(self):
        return self.title
    
    def increment_download(self):
        self.download_count += 1
        self.save()


class ContactMessage(models.Model):
    """View and manage contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    read_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    reply_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def mark_as_read(self, user=None):
        if not self.read:
            self.read = True
            self.read_at = timezone.now()
            self.read_by = user
            self.save()
