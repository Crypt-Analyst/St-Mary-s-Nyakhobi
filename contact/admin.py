from django.contrib import admin
from .models import ContactInquiry

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry_type', 'subject', 'submitted_at', 'is_replied', 'priority_level')
    list_filter = ('inquiry_type', 'is_replied', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_replied',)
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Administrative', {
            'fields': ('submitted_at', 'is_replied', 'admin_notes')
        }),
    )
    
    actions = ['mark_as_replied', 'mark_as_pending', 'export_inquiries']
    
    def priority_level(self, obj):
        """Determine priority based on inquiry type"""
        priority_map = {
            'admissions': '🔴 High',
            'academic': '🟡 Medium', 
            'general': '🟢 Low',
            'complaint': '🔴 High',
        }
        return priority_map.get(obj.inquiry_type, '🟢 Low')
    priority_level.short_description = 'Priority'
    
    def mark_as_replied(self, request, queryset):
        queryset.update(is_replied=True)
        self.message_user(request, f"{queryset.count()} inquiries marked as replied.")
    mark_as_replied.short_description = "Mark as replied"
    
    def mark_as_pending(self, request, queryset):
        queryset.update(is_replied=False)
        self.message_user(request, f"{queryset.count()} inquiries marked as pending.")
    mark_as_pending.short_description = "Mark as pending"
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-submitted_at')