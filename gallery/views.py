from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from .models import GalleryCategory, PhotoAlbum, Photo, PhotoLike, GallerySettings
import json

def gallery_home(request):
    """Main gallery page with featured albums and categories"""
    # Get featured albums
    featured_albums = PhotoAlbum.objects.filter(
        is_published=True, 
        is_featured=True
    ).select_related('category').prefetch_related('photos')[:6]
    
    # Get categories with album counts
    categories = GalleryCategory.objects.filter(
        is_active=True
    ).prefetch_related('albums')
    
    # Recent albums
    recent_albums = PhotoAlbum.objects.filter(
        is_published=True
    ).select_related('category').order_by('-created_at')[:8]
    
    # Gallery statistics
    stats = {
        'total_albums': PhotoAlbum.objects.filter(is_published=True).count(),
        'total_photos': Photo.objects.count(),
        'categories_count': categories.count(),
    }
    
    context = {
        'featured_albums': featured_albums,
        'categories': categories,
        'recent_albums': recent_albums,
        'stats': stats,
        'page_title': 'Photo Gallery'
    }
    
    return render(request, 'gallery/gallery_home.html', context)

def category_albums(request, slug):
    """Albums in a specific category"""
    category = get_object_or_404(GalleryCategory, slug=slug, is_active=True)
    
    albums_list = PhotoAlbum.objects.filter(
        category=category,
        is_published=True
    ).prefetch_related('photos').order_by('-created_at')
    
    # Pagination
    settings = GallerySettings.objects.first()
    per_page = settings.albums_per_page if settings else 9
    
    paginator = Paginator(albums_list, per_page)
    page_number = request.GET.get('page')
    albums = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'albums': albums,
        'page_title': f'{category.name} - Photo Gallery'
    }
    
    return render(request, 'gallery/category_albums.html', context)

def album_detail(request, slug):
    """Individual album with all photos"""
    album = get_object_or_404(
        PhotoAlbum.objects.select_related('category', 'created_by'),
        slug=slug,
        is_published=True
    )
    
    # Increment view count
    album.increment_views()
    
    # Get photos
    photos_list = album.photos.all().order_by('order', 'created_at')
    
    # Pagination
    settings = GallerySettings.objects.first()
    per_page = settings.photos_per_page if settings else 12
    
    paginator = Paginator(photos_list, per_page)
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)
    
    # Related albums
    related_albums = PhotoAlbum.objects.filter(
        category=album.category,
        is_published=True
    ).exclude(pk=album.pk).order_by('-created_at')[:4]
    
    context = {
        'album': album,
        'photos': photos,
        'related_albums': related_albums,
        'page_title': f'{album.title} - Photo Gallery'
    }
    
    return render(request, 'gallery/album_detail.html', context)

def photo_detail(request, album_slug, photo_id):
    """Individual photo view with navigation"""
    album = get_object_or_404(PhotoAlbum, slug=album_slug, is_published=True)
    photo = get_object_or_404(Photo, pk=photo_id, album=album)
    
    # Get navigation photos
    photos = list(album.photos.all().order_by('order', 'created_at'))
    current_index = photos.index(photo) if photo in photos else 0
    
    prev_photo = photos[current_index - 1] if current_index > 0 else None
    next_photo = photos[current_index + 1] if current_index < len(photos) - 1 else None
    
    context = {
        'album': album,
        'photo': photo,
        'prev_photo': prev_photo,
        'next_photo': next_photo,
        'current_index': current_index + 1,
        'total_photos': len(photos),
        'page_title': f'{photo.title or "Photo"} - {album.title}'
    }
    
    return render(request, 'gallery/photo_detail.html', context)

@require_POST
@csrf_exempt
def like_photo(request, photo_id):
    """AJAX endpoint to like a photo"""
    try:
        photo = get_object_or_404(Photo, pk=photo_id)
        
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Check if already liked
        like, created = PhotoLike.objects.get_or_create(
            photo=photo,
            ip_address=ip,
            defaults={'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200]}
        )
        
        if created:
            # Increment like count
            Photo.objects.filter(pk=photo_id).update(likes_count=F('likes_count') + 1)
            photo.refresh_from_db()
            return JsonResponse({
                'success': True,
                'liked': True,
                'likes_count': photo.likes_count
            })
        else:
            # Already liked
            return JsonResponse({
                'success': False,
                'message': 'Already liked',
                'liked': True,
                'likes_count': photo.likes_count
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error processing like'
        })

def search_gallery(request):
    """Search photos and albums"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'gallery/search_results.html', {
            'query': query,
            'page_title': 'Search Gallery'
        })
    
    # Search albums
    albums = PhotoAlbum.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_published=True
    ).select_related('category')[:10]
    
    # Search photos
    photos = Photo.objects.filter(
        Q(title__icontains=query) | Q(caption__icontains=query),
        album__is_published=True
    ).select_related('album', 'album__category')[:20]
    
    context = {
        'query': query,
        'albums': albums,
        'photos': photos,
        'albums_count': albums.count(),
        'photos_count': photos.count(),
        'page_title': f'Search results for "{query}"'
    }
    
    return render(request, 'gallery/search_results.html', context)

def download_photo(request, photo_id):
    """Download photo (if enabled in settings)"""
    settings = GallerySettings.objects.first()
    
    if not settings or not settings.allow_photo_download:
        messages.error(request, 'Photo downloads are not enabled.')
        return redirect('gallery:gallery_home')
    
    photo = get_object_or_404(Photo, pk=photo_id, album__is_published=True)
    
    try:
        response = HttpResponse(photo.image.read(), content_type='image/jpeg')
        filename = f"{photo.album.title}_{photo.title or photo.pk}.jpg"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        messages.error(request, 'Error downloading photo.')
        return redirect('gallery:photo_detail', 
                       album_slug=photo.album.slug, 
                       photo_id=photo.pk)
