from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import GalleryCategory, PhotoAlbum, Photo, PhotoLike, GallerySettings

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'album_count', 'icon', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def album_count(self, obj):
        count = obj.albums.count()
        if count > 0:
            url = reverse('admin:gallery_photoalbum_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} albums</a>', url, count)
        return '0 albums'
    album_count.short_description = 'Albums'

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    fields = ('title', 'image', 'thumbnail_preview', 'order', 'is_cover_photo')
    readonly_fields = ('thumbnail_preview',)
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', 
                             obj.thumbnail.url)
        elif obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', 
                             obj.image.url)
        return 'No image'
    thumbnail_preview.short_description = 'Preview'

@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'photo_count_display', 'cover_preview', 
                   'is_featured', 'is_published', 'views_count', 'event_date', 'created_at')
    list_filter = ('category', 'is_featured', 'is_published', 'event_date', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'event_date'
    inlines = [PhotoInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Event Details', {
            'fields': ('event_date', 'cover_photo')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('views_count',)
    
    def cover_preview(self, obj):
        if obj.cover_photo:
            return format_html('<img src="{}" style="max-width: 60px; max-height: 60px; border-radius: 4px;" />', 
                             obj.cover_photo.url)
        return 'No cover'
    cover_preview.short_description = 'Cover'
    
    def photo_count_display(self, obj):
        count = obj.photo_count()
        if count > 0:
            return format_html('<strong>{}</strong> photos', count)
        return '0 photos'
    photo_count_display.short_description = 'Photos'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new album
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title_display', 'album', 'image_preview', 'order', 
                   'is_cover_photo', 'likes_count', 'uploaded_by', 'created_at')
    list_filter = ('album__category', 'album', 'is_cover_photo', 'taken_date', 'created_at')
    search_fields = ('title', 'caption', 'album__title', 'photographer')
    date_hierarchy = 'taken_date'
    
    fieldsets = (
        ('Photo Information', {
            'fields': ('album', 'title', 'caption', 'image', 'thumbnail')
        }),
        ('Organization', {
            'fields': ('order', 'is_cover_photo')
        }),
        ('Metadata', {
            'fields': ('photographer', 'taken_date'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('likes_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('thumbnail', 'likes_count')
    
    def image_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-width: 80px; max-height: 80px; border-radius: 4px;" />', 
                             obj.thumbnail.url)
        elif obj.image:
            return format_html('<img src="{}" style="max-width: 80px; max-height: 80px; border-radius: 4px;" />', 
                             obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'
    
    def title_display(self, obj):
        return obj.title or f"Photo {obj.order}" if obj.order else "Untitled"
    title_display.short_description = 'Title'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new photo
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(PhotoLike)
class PhotoLikeAdmin(admin.ModelAdmin):
    list_display = ('photo', 'ip_address', 'created_at')
    list_filter = ('created_at', 'photo__album__category')
    search_fields = ('photo__title', 'photo__album__title', 'ip_address')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False  # Likes are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Don't allow editing likes

@admin.register(GallerySettings)
class GallerySettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Display Settings', {
            'fields': ('photos_per_page', 'albums_per_page')
        }),
        ('Photo Settings', {
            'fields': ('max_photo_size_mb', 'thumbnail_quality', 'allow_photo_download')
        }),
        ('Watermark Settings', {
            'fields': ('watermark_enabled', 'watermark_text'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not GallerySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False  # Don't allow deletion of settings
