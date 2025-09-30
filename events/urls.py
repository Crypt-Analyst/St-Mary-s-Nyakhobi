from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.events_list, name='events'),
    path('news/', views.news_list, name='news'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
]