from django.contrib import admin
from .models import AdmissionApplication, AdmissionRequirement

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('student_first_name', 'student_last_name', 'grade_level', 'status', 'application_date')
    list_filter = ('status', 'grade_level', 'application_date')
    search_fields = ('student_first_name', 'student_last_name', 'parent_email')
    list_editable = ('status',)
    date_hierarchy = 'application_date'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_first_name', 'student_last_name', 'date_of_birth', 'grade_level')
        }),
        ('Parent/Guardian Information', {
            'fields': ('parent_first_name', 'parent_last_name', 'parent_email', 'parent_phone', 'address')
        }),
        ('Additional Information', {
            'fields': ('previous_school', 'medical_conditions', 'additional_notes')
        }),
        ('Application Status', {
            'fields': ('status',)
        }),
    )
    
    readonly_fields = ('application_date',)

@admin.register(AdmissionRequirement)
class AdmissionRequirementAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'requirement_title', 'is_mandatory')
    list_filter = ('grade_level', 'is_mandatory')
    search_fields = ('requirement_title',)