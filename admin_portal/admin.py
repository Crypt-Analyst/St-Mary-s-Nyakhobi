from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SchoolSettings, NewsAnnouncement, GalleryImage, 
    TeacherProfile, SchoolEvent, DownloadableFile, ContactMessage
)


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('school_name', 'school_motto', 'school_logo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
        ('About Us', {
            'fields': ('about_text', 'vision', 'mission')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SchoolSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Never allow deletion
        return False


@admin.register(NewsAnnouncement)
class NewsAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'featured', 'created_at', 'created_by']
    list_filter = ['category', 'published', 'featured', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['published', 'featured']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'category', 'content', 'image')
        }),
        ('Settings', {
            'fields': ('published', 'featured')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'featured', 'image_preview', 'uploaded_at']
    list_filter = ['media_type', 'category', 'featured', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['featured']
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'media_type', 'category')
        }),
        ('Media', {
            'fields': ('image', 'video_url')
        }),
        ('Settings', {
            'fields': ('featured',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'department', 'subjects', 'is_active', 'photo_preview']
    list_filter = ['department', 'is_active']
    search_fields = ['name', 'position', 'subjects', 'qualifications']
    list_editable = ['is_active']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'department', 'photo')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Professional Details', {
            'fields': ('subjects', 'qualifications', 'bio')
        }),
        ('Settings', {
            'fields': ('is_active', 'display_order')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = 'Photo'


@admin.register(SchoolEvent)
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'end_date', 'location', 'published', 'created_by']
    list_filter = ['event_type', 'published', 'start_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['published']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'event_type', 'description', 'location')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date', 'start_time', 'end_time', 'all_day')
        }),
        ('Settings', {
            'fields': ('published',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DownloadableFile)
class DownloadableFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'file_size', 'download_count', 'published', 'uploaded_at']
    list_filter = ['category', 'published', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['published']
    date_hierarchy = 'uploaded_at'
    readonly_fields = ['download_count']
    
    fieldsets = (
        ('File Information', {
            'fields': ('title', 'category', 'description', 'file', 'file_size')
        }),
        ('Settings', {
            'fields': ('published', 'download_count')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        # Auto-calculate file size
        if obj.file:
            size_bytes = obj.file.size
            if size_bytes < 1024:
                obj.file_size = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                obj.file_size = f"{size_bytes / 1024:.1f} KB"
            else:
                obj.file_size = f"{size_bytes / (1024 * 1024):.1f} MB"
        super().save_model(request, obj, form, change)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'read_status', 'replied']
    list_filter = ['read', 'replied', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'submitted_at']
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'submitted_at')
        }),
        ('Status', {
            'fields': ('read', 'replied', 'reply_notes')
        }),
    )
    
    def read_status(self, obj):
        if obj.read:
            return format_html('<span style="color: green;">✓ Read</span>')
        return format_html('<span style="color: orange;">● Unread</span>')
    read_status.short_description = 'Status'
    
    def has_add_permission(self, request):
        # Don't allow manual creation - only from contact form
        return False
    
    def save_model(self, request, obj, form, change):
        if change and 'read' in form.changed_data and obj.read:
            obj.mark_as_read(request.user)
        else:
            super().save_model(request, obj, form, change)


# Customize admin site header
admin.site.site_header = "St. Mary's Nyakhobi Admin Portal"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "School Management Dashboard"
