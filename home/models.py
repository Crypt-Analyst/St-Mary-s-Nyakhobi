from django.db import models
from django.utils import timezone

class SchoolInfo(models.Model):
    """Basic school information for the homepage"""
    name = models.CharField(max_length=200, default="St. Mary's Nyakhobi Senior School")
    tagline = models.CharField(max_length=300, default="Building Leaders for Tomorrow", help_text="Short description of the school")
    welcome_message = models.TextField(default="St. Mary's Nyakhobi Senior School is a Sub-County public mixed day school committed to academic excellence, discipline and community service.", help_text="Welcome message for homepage")
    mission_statement = models.TextField(default="To provide quality, holistic education that develops academic excellence, discipline, character, and life skills in our students, preparing them to be responsible leaders and productive citizens in their communities and beyond.")
    vision_statement = models.TextField(default="To be a leading educational institution in Busia County that builds leaders for tomorrow through academic excellence, community service, and character development.")
    established_year = models.IntegerField(default=1980)
    phone = models.CharField(max_length=50, default="+254 722 231798 / +254 723 273109")
    email = models.EmailField(default="nyakhobisecondaryschool@gmail.com")
    address = models.TextField(default="Off Nambuku/Funyula Rd, Funyula, P.O. Box 254, Funyula 50406, Busia County, Kenya")
    
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