from django.contrib import admin
from .models import Event, News

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'end_date', 'event_type', 'location', 'is_published')
    list_filter = ('event_type', 'is_published', 'event_date')
    search_fields = ('title', 'description', 'location')
    list_editable = ('is_published',)
    date_hierarchy = 'event_date'
    ordering = ('-event_date',)
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'image')
        }),
        ('Date & Time', {
            'fields': ('event_date', 'end_date')
        }),
        ('Location & Type', {
            'fields': ('location', 'event_type')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
    )
    
    actions = ['publish_events', 'unpublish_events']
    
    def publish_events(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} events published.")
    publish_events.short_description = "Publish selected events"
    
    def unpublish_events(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} events unpublished.")
    unpublish_events.short_description = "Unpublish selected events"

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'summary')
    list_editable = ('is_published', 'is_featured')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'summary', 'content', 'image')
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured')
        }),
    )
    
    actions = ['make_featured', 'remove_featured', 'publish_news']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} news articles featured.")
    make_featured.short_description = "Feature selected news"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} news articles unfeatured.")
    remove_featured.short_description = "Unfeature selected news"
    
    def publish_news(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} news articles published.")
    publish_news.short_description = "Publish selected news"

