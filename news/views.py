from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import NewsArticle, NewsCategory, Newsletter

def news_home(request):
    """Main news page"""
    # Get featured articles
    featured_articles = NewsArticle.objects.filter(
        is_published=True, is_featured=True
    ).select_related('category', 'author')[:3]
    
    # Get recent articles
    recent_articles = NewsArticle.objects.filter(
        is_published=True
    ).select_related('category', 'author')[:6]
    
    # Get categories
    categories = NewsCategory.objects.filter(is_active=True)
    
    context = {
        'featured_articles': featured_articles,
        'recent_articles': recent_articles, 
        'categories': categories,
        'page_title': 'School News & Updates'
    }
    return render(request, 'news/news_home.html', context)

def article_detail(request, slug):
    """Individual article view"""
    article = get_object_or_404(
        NewsArticle.objects.select_related('category', 'author'),
        slug=slug, is_published=True
    )
    
    # Increment view count
    article.increment_views()
    
    # Get related articles
    related_articles = NewsArticle.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(pk=article.pk)[:4]
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'page_title': article.title
    }
    return render(request, 'news/article_detail.html', context)

def category_articles(request, slug):
    """Articles in a specific category"""
    category = get_object_or_404(NewsCategory, slug=slug, is_active=True)
    
    articles_list = NewsArticle.objects.filter(
        category=category, is_published=True
    ).select_related('author')
    
    paginator = Paginator(articles_list, 10)
    page = paginator.get_page(request.GET.get('page'))
    
    context = {
        'category': category,
        'articles': page,
        'page_title': f'{category.name} - News'
    }
    return render(request, 'news/category_articles.html', context)

def newsletters(request):
    """Newsletter archive"""
    newsletters_list = Newsletter.objects.filter(is_published=True)
    
    paginator = Paginator(newsletters_list, 12)
    page = paginator.get_page(request.GET.get('page'))
    
    context = {
        'newsletters': page,
        'page_title': 'School Newsletters'
    }
    return render(request, 'news/newsletters.html', context)
