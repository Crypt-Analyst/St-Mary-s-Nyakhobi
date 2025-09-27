from django.contrib import admin
from .models import SchoolInfo, HomePageSlider, QuickLink

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    
@admin.register(HomePageSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')

@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')