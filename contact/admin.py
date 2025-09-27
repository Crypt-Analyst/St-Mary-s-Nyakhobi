from django.contrib import admin
from .models import ContactInquiry

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry_type', 'subject', 'submitted_at', 'is_replied')
    list_filter = ('inquiry_type', 'is_replied', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_replied',)
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at',)