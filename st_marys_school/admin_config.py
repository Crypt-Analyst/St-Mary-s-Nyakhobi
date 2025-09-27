"""
Custom Django Admin Configuration for St. Mary's Nyakhobi Senior School
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html

class StMarysAdminSite(AdminSite):
    site_title = "St. Mary's Nyakhobi Admin"
    site_header = "St. Mary's Nyakhobi Senior School Administration"
    index_title = "School Management Dashboard"
    
    def index(self, request, extra_context=None):
        """
        Custom admin index with school-specific dashboard
        """
        extra_context = extra_context or {}
        
        # Add custom dashboard data
        from home.models import SchoolInfo
        from faculty.models import Faculty
        from events.models import Event
        from contact.models import ContactInquiry
        from django.utils import timezone
        from datetime import timedelta
        
        try:
            school_info = SchoolInfo.objects.first()
            
            # Dashboard statistics
            total_faculty = Faculty.objects.filter(is_active=True).count()
            upcoming_events = Event.objects.filter(
                event_date__gte=timezone.now(),
                is_published=True
            ).count()
            pending_inquiries = ContactInquiry.objects.filter(is_replied=False).count()
            recent_inquiries = ContactInquiry.objects.filter(
                submitted_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            
            extra_context.update({
                'school_info': school_info,
                'dashboard_stats': {
                    'total_faculty': total_faculty,
                    'upcoming_events': upcoming_events,
                    'pending_inquiries': pending_inquiries,
                    'recent_inquiries': recent_inquiries,
                }
            })
        except Exception:
            pass
            
        return super().index(request, extra_context)

# Create custom admin site instance
admin_site = StMarysAdminSite(name='stmarys_admin')

# Customize the default admin site
admin.site.site_title = "St. Mary's Nyakhobi Admin"
admin.site.site_header = "St. Mary's Nyakhobi Senior School Administration"
admin.site.index_title = "School Management Dashboard"

# Add custom CSS and JavaScript
def admin_custom_styles():
    return format_html('''
        <style>
            #header {
                background: linear-gradient(135deg, #800000, #a0002a);
                color: white;
            }
            #header h1 {
                color: #FFD700;
            }
            #header a:link, #header a:visited {
                color: #FFD700;
            }
            .module h2, .module caption, .inline-group h2 {
                background: #800000;
                color: white;
            }
            .button, input[type=submit], input[type=button], .submit-row input, a.button {
                background: #800000;
                border-color: #800000;
            }
            .button:hover, input[type=submit]:hover, input[type=button]:hover, .submit-row input:hover, a.button:hover {
                background: #a0002a;
                border-color: #a0002a;
            }
            .selector-available h2, .selector-chosen h2 {
                background: #800000;
                color: white;
            }
        </style>
    ''')

# Custom admin template tags
from django import template
register = template.Library()

@register.simple_tag
def admin_custom_styles_tag():
    return admin_custom_styles()