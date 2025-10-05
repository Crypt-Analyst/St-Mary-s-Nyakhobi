from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SchoolSettings, NewsAnnouncement, GalleryImage, 
    TeacherProfile, SchoolEvent, DownloadableFile, ContactMessage,
    HomePageBanner, AcademicDepartment, CurriculumInfo, AdmissionInfo,
    ParentInfo, SchoolValue, Newsletter, NewsletterSubscription, AdminActivityLog
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


@admin.register(HomePageBanner)
class HomePageBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'display_order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle', 'description']
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', '-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description', 'image')
        }),
        ('Call to Action', {
            'fields': ('button_text', 'button_link')
        }),
        ('Settings', {
            'fields': ('is_active', 'display_order')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 45px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(AcademicDepartment)
class AcademicDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head_of_department', 'display_order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'head_of_department', 'subjects_offered']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'description', 'head_of_department', 'department_image')
        }),
        ('Subjects', {
            'fields': ('subjects_offered',)
        }),
        ('Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )


@admin.register(CurriculumInfo)
class CurriculumInfoAdmin(admin.ModelAdmin):
    list_display = ['level', 'updated_at', 'updated_by']
    list_filter = ['level']
    ordering = ['level']
    
    fieldsets = (
        ('Level Information', {
            'fields': ('level', 'description')
        }),
        ('Subjects', {
            'fields': ('core_subjects', 'elective_subjects')
        }),
        ('Documents', {
            'fields': ('curriculum_file',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ['info_type', 'title', 'is_published', 'updated_at']
    list_filter = ['info_type', 'is_published']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    
    fieldsets = (
        ('Information Type', {
            'fields': ('info_type', 'title')
        }),
        ('Content', {
            'fields': ('content', 'application_form')
        }),
        ('Settings', {
            'fields': ('is_published',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ParentInfo)
class ParentInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'display_order', 'updated_at']
    list_filter = ['category', 'is_published']
    search_fields = ['title', 'content']
    list_editable = ['is_published', 'display_order']
    ordering = ['category', 'display_order']
    
    fieldsets = (
        ('Information', {
            'fields': ('category', 'title', 'content', 'attachment')
        }),
        ('Settings', {
            'fields': ('is_published', 'display_order')
        }),
    )


@admin.register(SchoolValue)
class SchoolValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_order', 'is_active', 'icon_class']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order']
    
    fieldsets = (
        ('Value Information', {
            'fields': ('title', 'description', 'icon_class')
        }),
        ('Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'is_published', 'sent_date', 'created_by', 'created_at']
    list_filter = ['is_published', 'sent_date', 'created_at']
    search_fields = ['subject', 'content']
    list_editable = ['is_published']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Newsletter Content', {
            'fields': ('subject', 'content', 'pdf_file')
        }),
        ('Status', {
            'fields': ('is_published', 'sent_date')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    date_hierarchy = 'subscribed_at'
    ordering = ['-subscribed_at']
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'name')
        }),
        ('Status', {
            'fields': ('is_active', 'unsubscribed_at')
        }),
    )


@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'content_type', 'object_repr', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp', 'user']
    search_fields = ['user__username', 'content_type', 'object_repr', 'description']
    date_hierarchy = 'timestamp'
    readonly_fields = ['user', 'action', 'content_type', 'object_id', 'object_repr', 
                       'description', 'ip_address', 'timestamp']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        # Logs are auto-generated, not manually created
        return False
    
    def has_change_permission(self, request, obj=None):
        # Logs should not be editable
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion of old logs for cleanup
        return request.user.is_superuser


# Customize admin site header
admin.site.site_header = "St. Mary's Nyakhobi Admin Portal"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "School Management Dashboard"
