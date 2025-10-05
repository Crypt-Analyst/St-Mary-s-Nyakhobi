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


class HomePageBanner(models.Model):
    """Homepage slider/banner management"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True, help_text="e.g., 'Learn More', 'Apply Now'")
    button_link = models.CharField(max_length=200, blank=True, help_text="URL or page path")
    
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Homepage Banner'
        verbose_name_plural = 'Homepage Banners'
    
    def __str__(self):
        return self.title


class AcademicDepartment(models.Model):
    """Academic departments and subjects"""
    name = models.CharField(max_length=100, help_text="e.g., Sciences, Languages, Mathematics")
    description = models.TextField()
    head_of_department = models.CharField(max_length=200, blank=True)
    
    subjects_offered = models.TextField(help_text="List all subjects in this department")
    department_image = models.ImageField(upload_to='academics/', blank=True, null=True)
    
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Academic Department'
        verbose_name_plural = 'Academic Departments'
    
    def __str__(self):
        return self.name


class CurriculumInfo(models.Model):
    """Curriculum and academic program information"""
    LEVEL_CHOICES = [
        ('form1', 'Form 1'),
        ('form2', 'Form 2'),
        ('form3', 'Form 3'),
        ('form4', 'Form 4'),
    ]
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)
    description = models.TextField(help_text="Overview of this level")
    core_subjects = models.TextField(help_text="List core/compulsory subjects")
    elective_subjects = models.TextField(blank=True, help_text="List optional subjects")
    
    curriculum_file = models.FileField(upload_to='curriculum/', blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['level']
        verbose_name = 'Curriculum Information'
        verbose_name_plural = 'Curriculum Information'
    
    def __str__(self):
        return f"{self.get_level_display()} Curriculum"


class AdmissionInfo(models.Model):
    """Admissions requirements and information"""
    INFO_TYPE_CHOICES = [
        ('requirements', 'Admission Requirements'),
        ('process', 'Application Process'),
        ('fees', 'Fee Structure'),
        ('documents', 'Required Documents'),
        ('deadlines', 'Important Dates'),
    ]
    
    info_type = models.CharField(max_length=20, choices=INFO_TYPE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Detailed information")
    
    application_form = models.FileField(upload_to='admissions/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Admission Information'
        verbose_name_plural = 'Admission Information'
    
    def __str__(self):
        return self.title


class ParentInfo(models.Model):
    """Parent information - fees, policies, uniform, etc."""
    CATEGORY_CHOICES = [
        ('fees', 'Fees & Payments'),
        ('uniform', 'Uniform Requirements'),
        ('policy', 'School Policies'),
        ('calendar', 'Academic Calendar'),
        ('transport', 'Transport Information'),
        ('general', 'General Information'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    attachment = models.FileField(upload_to='parent_info/', blank=True, null=True, 
                                  help_text="PDF or document file")
    
    is_published = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'display_order']
        verbose_name = 'Parent Information'
        verbose_name_plural = 'Parent Information'
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.title}"


class SchoolValue(models.Model):
    """Core values and principles"""
    title = models.CharField(max_length=100, help_text="e.g., Integrity, Excellence, Respect")
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, 
                                  help_text="Font Awesome icon class, e.g., 'fas fa-star'")
    
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order']
        verbose_name = 'School Value'
        verbose_name_plural = 'School Values'
    
    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """Newsletter management and subscriptions"""
    subject = models.CharField(max_length=200)
    content = models.TextField()
    
    pdf_file = models.FileField(upload_to='newsletters/', blank=True, null=True)
    
    sent_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_newsletters')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
    
    def __str__(self):
        return self.subject


class NewsletterSubscription(models.Model):
    """Newsletter subscriber management"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
    
    def __str__(self):
        return self.email


class AdminActivityLog(models.Model):
    """Track admin actions for security and auditing"""
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('login', 'Logged In'),
        ('logout', 'Logged Out'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content_type = models.CharField(max_length=100, help_text="Type of content modified")
    object_id = models.IntegerField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True)
    
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.content_type} at {self.timestamp}"
