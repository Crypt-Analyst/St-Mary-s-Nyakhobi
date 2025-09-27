from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('', views.admission_info, name='info'),
    path('apply/', views.apply, name='apply'),
    path('requirements/', views.requirements, name='requirements'),
]