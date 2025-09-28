from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils import timezone

class GalleryCategory(models.Model):
    """Categories for organizing photo albums"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default='fas fa-images', 
                          help_text='Font Awesome icon class')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Gallery Categories"

class PhotoAlbum(models.Model):
    """Photo albums for different events and activities"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, 
                               related_name='albums')
    cover_photo = models.ImageField(upload_to='gallery/covers/', blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    event_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False, 
                                    help_text='Show in featured albums section')
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('gallery:album_detail', kwargs={'slug': self.slug})
    
    def photo_count(self):
        return self.photos.count()
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', '-created_at']),
        ]

class Photo(models.Model):
    """Individual photos in albums"""
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, 
                            related_name='photos')
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/photos/')
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True)
    order = models.PositiveIntegerField(default=0, 
                                      help_text='Order in which photos appear')
    photographer = models.CharField(max_length=100, blank=True)
    taken_date = models.DateTimeField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_cover_photo = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.album.title} - Photo {self.order or 'Untitled'}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Generate thumbnail if it doesn't exist
        if self.image and not self.thumbnail:
            self.create_thumbnail()
        
        # Set as album cover if marked as cover photo
        if self.is_cover_photo:
            self.album.cover_photo = self.image
            self.album.save(update_fields=['cover_photo'])
    
    def create_thumbnail(self):
        """Create thumbnail image"""
        if not self.image:
            return
        
        from PIL import Image
        from django.core.files.base import ContentFile
        from io import BytesIO
        import os
        
        # Open original image
        image = Image.open(self.image)
        image = image.convert('RGB')
        
        # Create thumbnail
        thumbnail_size = (300, 200)
        image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Save thumbnail
        thumb_io = BytesIO()
        image.save(thumb_io, format='JPEG', quality=85)
        
        # Generate thumbnail filename
        name, ext = os.path.splitext(self.image.name)
        thumbnail_name = f"{name}_thumb{ext}"
        
        self.thumbnail.save(
            thumbnail_name,
            ContentFile(thumb_io.getvalue()),
            save=False
        )
    
    class Meta:
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['album', 'order']),
        ]

class PhotoLike(models.Model):
    """Track photo likes from visitors"""
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['photo', 'ip_address']
        indexes = [
            models.Index(fields=['photo', 'ip_address']),
        ]

class GallerySettings(models.Model):
    """Gallery configuration settings"""
    photos_per_page = models.PositiveIntegerField(default=12)
    albums_per_page = models.PositiveIntegerField(default=9)
    allow_photo_download = models.BooleanField(default=False)
    watermark_enabled = models.BooleanField(default=False)
    watermark_text = models.CharField(max_length=100, 
                                    default='St. Mary\'s Nyakhobi School')
    max_photo_size_mb = models.PositiveIntegerField(default=5)
    thumbnail_quality = models.PositiveIntegerField(default=85)
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and GallerySettings.objects.exists():
            raise ValueError('Gallery settings already exist')
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Gallery Settings"
        verbose_name_plural = "Gallery Settings"
