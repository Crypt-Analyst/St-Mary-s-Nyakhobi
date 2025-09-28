from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
import os

class NewsCategory(models.Model):
    """Categories for organizing news articles"""
    CATEGORY_TYPES = [
        ('announcement', 'School Announcements'),
        ('achievement', 'Student Achievements'),
        ('event', 'Upcoming Events'),
        ('academic', 'Academic News'),
        ('sports', 'Sports News'),
        ('community', 'Community News'),
        ('administration', 'Administration Updates'),
        ('general', 'General News'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='general')
    color = models.CharField(max_length=7, default='#800000', help_text='Hex color code for category')
    icon = models.CharField(max_length=50, default='fas fa-newspaper', help_text='Font Awesome icon class')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "News Categories"

class NewsArticle(models.Model):
    """News articles and blog posts"""
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('normal', 'Normal Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True, help_text='Optional subtitle or summary')
    content = models.TextField(help_text='Article content in HTML format')
    excerpt = models.TextField(max_length=500, blank=True, help_text='Short description for previews')
    
    # Categorization
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='articles')
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    
    # Media
    featured_image = models.ImageField(upload_to='news/images/', blank=True)
    image_caption = models.CharField(max_length=200, blank=True)
    
    # Publishing
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False, help_text='Show in featured news section')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Timestamps
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO and Social
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO meta description')
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            from django.utils.html import strip_tags
            self.excerpt = strip_tags(self.content)[:497] + "..."
        
        # Set published date when first published
        if self.is_published and not self.published_date:
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', '-published_date']),
            models.Index(fields=['category', '-published_date']),
        ]

class Newsletter(models.Model):
    """School newsletters"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    # Publication details
    volume = models.PositiveIntegerField(help_text='Newsletter volume/year')
    issue = models.PositiveIntegerField(help_text='Issue number')
    publication_date = models.DateField()
    
    # Files
    pdf_file = models.FileField(upload_to='newsletters/pdf/', blank=True)
    cover_image = models.ImageField(upload_to='newsletters/covers/', blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - Vol.{self.volume} Issue {self.issue}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-vol{self.volume}-issue{self.issue}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:newsletter_detail', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ['-publication_date']
        unique_together = ['volume', 'issue']

class ArticleLike(models.Model):
    """Track article likes"""
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['article', 'ip_address']

class Comment(models.Model):
    """Comments on news articles"""
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    
    # Metadata
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.name} on {self.article.title}"
    
    class Meta:
        ordering = ['-created_at']

class NewsSettings(models.Model):
    """News system settings"""
    articles_per_page = models.PositiveIntegerField(default=10)
    allow_comments = models.BooleanField(default=True)
    moderate_comments = models.BooleanField(default=True)
    show_author_info = models.BooleanField(default=True)
    enable_social_sharing = models.BooleanField(default=True)
    newsletter_signup_enabled = models.BooleanField(default=True)
    
    # SEO Settings
    site_name = models.CharField(max_length=100, default="St. Mary's Nyakhobi School News")
    default_meta_description = models.CharField(max_length=160, 
                                              default="Latest news, announcements, and updates from St. Mary's Nyakhobi School")
    
    def save(self, *args, **kwargs):
        if not self.pk and NewsSettings.objects.exists():
            raise ValueError('News settings already exist')
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "News Settings"
        verbose_name_plural = "News Settings"
