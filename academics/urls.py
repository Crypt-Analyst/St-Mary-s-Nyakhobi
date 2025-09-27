from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.programs, name='programs'),
    path('calendar/', views.academic_calendar, name='calendar'),
    path('program/<int:program_id>/', views.program_detail, name='program_detail'),
]