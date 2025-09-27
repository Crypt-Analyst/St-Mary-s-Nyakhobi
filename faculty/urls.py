from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    path('', views.faculty_list, name='faculty_list'),
    path('department/<int:department_id>/', views.department_detail, name='department_detail'),
]