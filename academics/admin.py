from django.contrib import admin
from .models import GradeLevel, Subject, AcademicProgram, AcademicCalendar

@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'age_range')
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('grade_levels',)

@admin.register(AcademicProgram)
class AcademicProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration')
    search_fields = ('name',)
    filter_horizontal = ('grade_levels', 'subjects')

@admin.register(AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_holiday')
    list_filter = ('is_holiday', 'start_date')
    date_hierarchy = 'start_date'