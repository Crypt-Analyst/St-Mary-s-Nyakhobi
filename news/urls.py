from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Main news pages
    path('', views.news_home, name='news_home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category_articles, name='category_articles'),
    
    # Newsletter pages
    path('newsletters/', views.newsletters, name='newsletters'),
    path('newsletter/<slug:slug>/', views.newsletter_detail, name='newsletter_detail'),
    
    # Search and utilities
    path('search/', views.search_news, name='search_news'),
    path('archive/', views.news_archive, name='news_archive'),
    
    # AJAX endpoints
    path('like/<int:article_id>/', views.like_article, name='like_article'),
    path('comment/add/', views.add_comment, name='add_comment'),
]