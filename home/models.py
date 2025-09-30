from django.db import models
from django.utils import timezone

class SchoolInfo(models.Model):
    """Basic school information for the homepage"""
    name = models.CharField(max_length=200, default="St. Mary's Nyakhobi Senior School")
    tagline = models.CharField(max_length=300, default="Building Leaders for Tomorrow", help_text="Short description of the school")
    welcome_message = models.TextField(default="St. Mary's Nyakhobi Senior School (formerly Nyakhobi Secondary School) is located in Nyakhobi Sub-location, Namboboto Location, Samia Sub-County, Busia County, Kenya. The school is sponsored by ACK Church Nambale Diocese and started in 1983 with 6 students.", help_text="Welcome message for homepage")
    mission_statement = models.TextField(default="To consistently provide quality secondary education.")
    vision_statement = models.TextField(default="To be an institution of excellence in pursuit of quality and holistic education.")
    established_year = models.IntegerField(default=1983)
    phone = models.CharField(max_length=50, default="+254 719 831 346")
    email = models.EmailField(default="nyakhobisecsch@gmail.com")
    address = models.TextField(default="P.O. Box 254-50406, Funyula, Nyakhobi Sub-location, Namboboto Location, Samia Sub-County, Busia County, Kenya")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "School Information"
        verbose_name_plural = "School Information"

class HomePageSlider(models.Model):
    """Image slider for homepage"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='slider/')
    link_text = models.CharField(max_length=50, blank=True)
    link_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']

class QuickLink(models.Model):
    """Quick links section on homepage"""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    link_url = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']