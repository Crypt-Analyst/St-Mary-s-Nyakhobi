from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db import models
from django.forms import Textarea
from .models import NewsCategory, NewsArticle, Newsletter, ArticleLike, Comment, NewsSettings

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'article_count', 'color_preview', 'is_active', 'order')
    list_filter = ('category_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    
    def article_count(self, obj):
        count = obj.articles.filter(is_published=True).count()
        if count > 0:
            url = reverse('admin:news_newsarticle_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} articles</a>', url, count)
        return '0 articles'
    article_count.short_description = 'Published Articles'
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'priority_badge', 'status_badge', 
                   'views_count', 'likes_count', 'published_date', 'created_at')
    list_filter = ('category', 'is_published', 'is_featured', 'priority', 'created_at', 'published_date')
    search_fields = ('title', 'content', 'excerpt', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'subtitle', 'excerpt', 'content')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_caption'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'priority', 'published_date')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('views_count', 'likes_count')
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
    }
    
    def priority_badge(self, obj):
        colors = {
            'urgent': '#dc3545',
            'high': '#fd7e14', 
            'normal': '#6c757d',
            'low': '#20c997'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.priority, '#6c757d'),
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    def status_badge(self, obj):
        if obj.is_published:
            badge_class = 'background-color: #28a745; color: white;'
            text = 'Published'
            if obj.is_featured:
                text = '⭐ Featured'
        else:
            badge_class = 'background-color: #6c757d; color: white;'
            text = 'Draft'
        
        return format_html(
            '<span style="{}; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            badge_class, text
        )
    status_badge.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new article
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} articles were published.')
    make_published.short_description = "Publish selected articles"
    
    def make_draft(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} articles were moved to draft.')
    make_draft.short_description = "Move to draft"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} articles were marked as featured.')
    make_featured.short_description = "Mark as featured"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'volume', 'issue', 'publication_date', 'file_preview', 
                   'is_published', 'is_featured', 'created_at')
    list_filter = ('is_published', 'is_featured', 'publication_date', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publication_date'
    
    fieldsets = (
        ('Newsletter Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Publication Details', {
            'fields': ('volume', 'issue', 'publication_date')
        }),
        ('Files', {
            'fields': ('pdf_file', 'cover_image')
        }),
        ('Settings', {
            'fields': ('is_published', 'is_featured')
        }),
    )
    
    def file_preview(self, obj):
        if obj.pdf_file:
            return format_html(
                '<a href="{}" target="_blank" title="Download PDF">📄 PDF Available</a>',
                obj.pdf_file.url
            )
        return 'No file'
    file_preview.short_description = 'PDF File'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new newsletter
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'content_preview', 'is_approved', 'is_spam', 'created_at')
    list_filter = ('is_approved', 'is_spam', 'created_at', 'article__category')
    search_fields = ('name', 'email', 'content', 'article__title')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('article', 'name', 'email', 'website', 'content')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_spam')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('ip_address', 'user_agent')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    actions = ['approve_comments', 'mark_as_spam']
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True, is_spam=False)
        self.message_user(request, f'{updated} comments were approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def mark_as_spam(self, request, queryset):
        updated = queryset.update(is_spam=True, is_approved=False)
        self.message_user(request, f'{updated} comments were marked as spam.')
    mark_as_spam.short_description = "Mark as spam"

@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'ip_address', 'created_at')
    list_filter = ('created_at', 'article__category')
    search_fields = ('article__title', 'ip_address')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False  # Likes are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Don't allow editing likes

@admin.register(NewsSettings)
class NewsSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Display Settings', {
            'fields': ('articles_per_page', 'show_author_info', 'enable_social_sharing')
        }),
        ('Comment Settings', {
            'fields': ('allow_comments', 'moderate_comments')
        }),
        ('Newsletter', {
            'fields': ('newsletter_signup_enabled',)
        }),
        ('SEO Settings', {
            'fields': ('site_name', 'default_meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return not NewsSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
