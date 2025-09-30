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

def newsletter_detail(request, slug):
    """Individual newsletter view"""
    newsletter = get_object_or_404(Newsletter, slug=slug, is_published=True)
    
    context = {
        'newsletter': newsletter,
        'page_title': newsletter.title
    }
    return render(request, 'news/newsletter_detail.html', context)

def search_news(request):
    """Search news articles"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'news/search_results.html', {
            'query': query,
            'page_title': 'Search News'
        })
    
    # Search articles
    articles = NewsArticle.objects.filter(
        Q(title__icontains=query) | 
        Q(content__icontains=query) | 
        Q(excerpt__icontains=query) |
        Q(tags__icontains=query),
        is_published=True
    ).select_related('category', 'author')
    
    paginator = Paginator(articles, 10)
    page = paginator.get_page(request.GET.get('page'))
    
    context = {
        'query': query,
        'articles': page,
        'total_results': articles.count(),
        'page_title': f'Search results for "{query}"'
    }
    return render(request, 'news/search_results.html', context)

def news_archive(request):
    """News archive by date"""
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    articles = NewsArticle.objects.filter(is_published=True)
    
    if year:
        articles = articles.filter(published_date__year=year)
    if month:
        articles = articles.filter(published_date__month=month)
    
    articles = articles.select_related('category', 'author')
    
    paginator = Paginator(articles, 15)
    page = paginator.get_page(request.GET.get('page'))
    
    # Get archive dates
    from django.db.models import Extract
    archive_dates = NewsArticle.objects.filter(
        is_published=True
    ).dates('published_date', 'month', order='DESC')
    
    context = {
        'articles': page,
        'archive_dates': archive_dates,
        'current_year': year,
        'current_month': month,
        'page_title': 'News Archive'
    }
    return render(request, 'news/news_archive.html', context)

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

@require_POST
@csrf_exempt
def like_article(request, article_id):
    """AJAX endpoint to like an article"""
    try:
        article = get_object_or_404(NewsArticle, pk=article_id, is_published=True)
        
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        from .models import ArticleLike
        # Check if already liked
        like, created = ArticleLike.objects.get_or_create(
            article=article,
            ip_address=ip,
            defaults={'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200]}
        )
        
        if created:
            # Increment like count
            NewsArticle.objects.filter(pk=article_id).update(likes_count=F('likes_count') + 1)
            article.refresh_from_db()
            return JsonResponse({
                'success': True,
                'liked': True,
                'likes_count': article.likes_count
            })
        else:
            # Already liked
            return JsonResponse({
                'success': False,
                'message': 'Already liked',
                'liked': True,
                'likes_count': article.likes_count
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error processing like'
        })

@require_POST
def add_comment(request):
    """Add a comment to an article"""
    from .models import Comment
    
    article_id = request.POST.get('article_id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    website = request.POST.get('website', '')
    content = request.POST.get('content')
    
    if not all([article_id, name, email, content]):
        return JsonResponse({
            'success': False,
            'message': 'All fields are required'
        })
    
    try:
        article = NewsArticle.objects.get(pk=article_id, is_published=True)
        
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        comment = Comment.objects.create(
            article=article,
            name=name,
            email=email,
            website=website,
            content=content,
            ip_address=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:200]
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Comment submitted successfully. It will be reviewed before being published.'
        })
        
    except NewsArticle.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Article not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error submitting comment'
        })
