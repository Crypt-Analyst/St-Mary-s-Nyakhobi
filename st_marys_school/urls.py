"""
URL configuration for st_marys_school project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('academics/', include('academics.urls')),
    path('admissions/', include('admissions.urls')),
    path('faculty/', include('faculty.urls')),
    path('events/', include('events.urls')),
    path('contact/', include('contact.urls')),
    path('gallery/', include('gallery.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)