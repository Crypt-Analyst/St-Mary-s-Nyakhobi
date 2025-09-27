from django.contrib import admin
from .models import SchoolInfo, HomePageSlider, QuickLink

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'established_year')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'established_year')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Mission & Vision', {
            'fields': ('welcome_message', 'mission_statement', 'vision_statement'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one school info instance
        return not SchoolInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of school info
        return False
    
@admin.register(HomePageSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'link_url')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')
    prepopulated_fields = {'link_url': ('title',)}
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'image')
        }),
        ('Link Settings', {
            'fields': ('link_text', 'link_url')
        }),
        ('Display Options', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order', 'link_url')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Link Settings', {
            'fields': ('link_url',)
        }),
        ('Display Options', {
            'fields': ('is_active', 'order')
        }),
    )
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',)
        }