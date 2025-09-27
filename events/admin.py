from django.contrib import admin
from .models import Event, News, Gallery

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_type', 'location', 'is_published')
    list_filter = ('event_type', 'is_published', 'event_date')
    search_fields = ('title', 'description')
    list_editable = ('is_published',)
    date_hierarchy = 'event_date'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'is_featured')
    date_hierarchy = 'created_at'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'uploaded_at')
    list_filter = ('uploaded_at', 'event')
    search_fields = ('title', 'description')