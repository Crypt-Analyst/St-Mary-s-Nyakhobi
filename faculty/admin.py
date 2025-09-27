from django.contrib import admin
from .models import Department, Faculty

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department')
    search_fields = ('name',)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'email', 'is_active')
    list_filter = ('position', 'department', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'photo', 'bio')
        }),
        ('Professional Information', {
            'fields': ('position', 'department', 'subjects_taught', 'qualifications', 'experience_years', 'joined_date')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )