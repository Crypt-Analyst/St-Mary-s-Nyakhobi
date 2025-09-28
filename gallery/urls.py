from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    # Main gallery pages
    path('', views.gallery_home, name='gallery_home'),
    path('category/<slug:slug>/', views.category_albums, name='category_albums'),
    path('album/<slug:slug>/', views.album_detail, name='album_detail'),
    path('album/<slug:album_slug>/photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    
    # Search and utilities
    path('search/', views.search_gallery, name='search_gallery'),
    path('download/<int:photo_id>/', views.download_photo, name='download_photo'),
    
    # AJAX endpoints
    path('like/<int:photo_id>/', views.like_photo, name='like_photo'),
]