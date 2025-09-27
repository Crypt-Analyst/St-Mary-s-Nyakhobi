from django.contrib import admin
from .models import Department, Faculty

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department')
    search_fields = ('name',)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'email', 'experience_years', 'is_active')
    list_filter = ('position', 'department', 'is_active', 'joined_date')
    search_fields = ('first_name', 'last_name', 'email', 'subjects_taught')
    list_editable = ('is_active',)
    date_hierarchy = 'joined_date'
    ordering = ('position', 'last_name', 'first_name')
    
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
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('department')
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} faculty members activated.")
    make_active.short_description = "Activate selected faculty"
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} faculty members deactivated.")
    make_inactive.short_description = "Deactivate selected faculty"