from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('mission-vision/', views.mission_vision, name='mission_vision'),
    path('facilities/', views.facilities, name='facilities'),
    path('achievements/', views.achievements, name='achievements'),
    path('leadership/', views.leadership, name='leadership'),
]