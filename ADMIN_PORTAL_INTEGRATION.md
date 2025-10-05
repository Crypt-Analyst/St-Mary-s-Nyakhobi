# Admin Portal Website Integration Guide

## Overview
This guide shows how to display content from the admin portal on your public website pages.

---

## ✅ What Works Now

The admin portal (`/admin/`) is **fully functional**:
- ✅ Add/edit/delete news, events, gallery, teachers, files
- ✅ All changes save to database
- ✅ Data persists across sessions
- ✅ Upload images and files

## ⚠️ What Needs Integration

Content added in admin portal doesn't automatically appear on public pages. You need to:
1. Update views to query admin_portal models
2. Update templates to display the data

---

## 🔧 Quick Integration Steps

### 1. Update News Page

**File: `events/views.py`**

```python
from django.shortcuts import render, get_object_or_404
from admin_portal.models import NewsAnnouncement, SchoolEvent  # NEW
from .models import Event, News  # OLD - can remove later

def news_list(request):
    """Display all news - using admin portal"""
    news = NewsAnnouncement.objects.filter(published=True).order_by('-created_at')
    
    context = {
        'news_items': news,  # Changed from 'news' to avoid template conflicts
    }
    return render(request, 'events/news_list.html', context)

def news_detail(request, news_id):
    """Display news details - using admin portal"""
    news_item = get_object_or_404(NewsAnnouncement, id=news_id, published=True)
    
    context = {
        'news_item': news_item,
    }
    return render(request, 'events/news_detail.html', context)
```

### 2. Update Events Page

```python
def events_list(request):
    """Display all events - using admin portal"""
    events = SchoolEvent.objects.filter(published=True).order_by('-start_date')
    
    context = {
        'events': events,
    }
    return render(request, 'events/calendar.html', context)

def event_detail(request, event_id):
    """Display event details - using admin portal"""
    event = get_object_or_404(SchoolEvent, id=event_id, published=True)
    
    context = {
        'event': event,
    }
    return render(request, 'events/event_detail.html', context)
```

### 3. Update Homepage

**File: `home/views.py`**

```python
from django.shortcuts import render
from admin_portal.models import NewsAnnouncement, SchoolSettings  # NEW
from .models import SchoolInfo, HomePageSlider, QuickLink

def home(request):
    """Homepage view"""
    # Get school settings from admin portal
    try:
        school_settings = SchoolSettings.objects.first()
    except:
        school_settings = None
    
    # OLD school info (can migrate to SchoolSettings)
    try:
        school_info = SchoolInfo.objects.first()
    except:
        school_info = None
    
    slider_images = HomePageSlider.objects.filter(is_active=True)
    quick_links = QuickLink.objects.filter(is_active=True)
    
    # Get latest news from admin portal
    latest_news = NewsAnnouncement.objects.filter(
        published=True
    ).order_by('-created_at')[:3]
    
    context = {
        'school_info': school_info,
        'school_settings': school_settings,  # NEW
        'slider_images': slider_images,
        'quick_links': quick_links,
        'latest_news': latest_news,
    }
    return render(request, 'home/index.html', context)
```

### 4. Create Gallery Page

**New file: `home/views.py` (add this function)**

```python
from admin_portal.models import GalleryImage

def gallery(request):
    """Gallery page using admin portal"""
    # Get photos
    photos = GalleryImage.objects.filter(
        published=True,
        media_type='photo'
    ).order_by('-uploaded_at')
    
    # Get videos
    videos = GalleryImage.objects.filter(
        published=True,
        media_type='video'
    ).order_by('-uploaded_at')
    
    context = {
        'photos': photos,
        'videos': videos,
    }
    return render(request, 'home/gallery.html', context)
```

### 5. Create Staff/Teachers Page

```python
from admin_portal.models import TeacherProfile

def faculty(request):
    """Faculty page using admin portal"""
    teachers = TeacherProfile.objects.filter(
        is_active=True
    ).order_by('display_order', 'name')
    
    # Group by department
    departments = {}
    for teacher in teachers:
        dept = teacher.department or 'Other'
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(teacher)
    
    context = {
        'teachers': teachers,
        'departments': departments,
    }
    return render(request, 'faculty/staff.html', context)
```

### 6. Create Downloads Page

```python
from admin_portal.models import DownloadableFile

def downloads(request):
    """Downloads page using admin portal"""
    files = DownloadableFile.objects.filter(
        published=True
    ).order_by('category', '-uploaded_at')
    
    # Group by category
    categories = {}
    for file in files:
        cat = file.get_category_display()
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(file)
    
    context = {
        'files': files,
        'categories': categories,
    }
    return render(request, 'home/downloads.html', context)
```

---

## 📝 Template Examples

### News List Template

```html
<!-- templates/events/news_list.html -->
{% for news in news_items %}
<div class="news-card">
    {% if news.image %}
    <img src="{{ news.image.url }}" alt="{{ news.title }}">
    {% endif %}
    
    <h3>{{ news.title }}</h3>
    <span class="badge">{{ news.get_category_display }}</span>
    
    <p>{{ news.content|truncatewords:30 }}</p>
    
    <small>Posted: {{ news.created_at|date:"F d, Y" }}</small>
    {% if news.created_by %}
    <small>By: {{ news.created_by.get_full_name }}</small>
    {% endif %}
    
    <a href="{% url 'events:news_detail' news.id %}">Read More</a>
</div>
{% empty %}
<p>No news available yet. Add news in the admin portal!</p>
{% endfor %}
```

### Gallery Template

```html
<!-- templates/home/gallery.html -->
<div class="row">
    {% for photo in photos %}
    <div class="col-md-4 mb-4">
        <div class="gallery-item">
            <img src="{{ photo.image.url }}" alt="{{ photo.title }}" class="img-fluid">
            <div class="overlay">
                <h5>{{ photo.title }}</h5>
                <p>{{ photo.description }}</p>
                <small>{{ photo.get_category_display }}</small>
            </div>
        </div>
    </div>
    {% endfor %}
</div>

<!-- Videos Section -->
<h2>Videos</h2>
<div class="row">
    {% for video in videos %}
    <div class="col-md-6 mb-4">
        <div class="video-card">
            <h4>{{ video.title }}</h4>
            <div class="embed-responsive embed-responsive-16by9">
                <iframe src="{{ video.video_url }}" allowfullscreen></iframe>
            </div>
            <p>{{ video.description }}</p>
        </div>
    </div>
    {% endfor %}
</div>
```

### Teachers List Template

```html
<!-- templates/faculty/staff.html -->
{% for department, teachers in departments.items %}
<div class="department-section">
    <h2>{{ department }}</h2>
    <div class="row">
        {% for teacher in teachers %}
        <div class="col-md-4 mb-4">
            <div class="teacher-card">
                {% if teacher.photo %}
                <img src="{{ teacher.photo.url }}" alt="{{ teacher.name }}">
                {% endif %}
                
                <h4>{{ teacher.name }}</h4>
                <p class="position">{{ teacher.position }}</p>
                
                {% if teacher.subjects %}
                <p><strong>Subjects:</strong> {{ teacher.subjects }}</p>
                {% endif %}
                
                {% if teacher.email %}
                <p><i class="fas fa-envelope"></i> {{ teacher.email }}</p>
                {% endif %}
                
                {% if teacher.phone %}
                <p><i class="fas fa-phone"></i> {{ teacher.phone }}</p>
                {% endif %}
                
                {% if teacher.qualifications %}
                <p><small>{{ teacher.qualifications }}</small></p>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endfor %}
```

### Downloads Page Template

```html
<!-- templates/home/downloads.html -->
{% for category, files in categories.items %}
<div class="download-category">
    <h2>{{ category }}</h2>
    <div class="list-group">
        {% for file in files %}
        <a href="{{ file.file.url }}" class="list-group-item list-group-item-action" download>
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h5>{{ file.title }}</h5>
                    {% if file.description %}
                    <p class="mb-0">{{ file.description }}</p>
                    {% endif %}
                </div>
                <div class="text-right">
                    <span class="badge badge-primary">{{ file.file_size_display }}</span>
                    <small class="d-block">{{ file.download_count }} downloads</small>
                    <small class="text-muted">{{ file.uploaded_at|date:"M d, Y" }}</small>
                </div>
            </div>
        </a>
        {% endfor %}
    </div>
</div>
{% endfor %}
```

---

## 🗄️ Data Migration (Optional)

If you have existing data in the old models, you can migrate it:

```python
# migration_script.py
from events.models import News as OldNews
from admin_portal.models import NewsAnnouncement

# Migrate old news to new system
for old_news in OldNews.objects.all():
    NewsAnnouncement.objects.create(
        title=old_news.title,
        content=old_news.content,
        image=old_news.image if hasattr(old_news, 'image') else None,
        category='news',
        published=old_news.is_published,
        created_at=old_news.created_at,
    )
```

---

## 🧹 Cleanup Old System (After Migration)

Once everything is integrated:

1. **Remove old apps** from `INSTALLED_APPS`:
   - Can keep `events` app but remove old models
   - Or migrate URLs to use new views

2. **Update URLs** in `st_marys_school/urls.py`:
   ```python
   # Old
   path('events/', include('events.urls')),
   
   # New - point to updated views using admin_portal models
   # No changes needed if events/views.py is updated
   ```

3. **Remove old models** (optional):
   - Keep for backward compatibility
   - Or delete and remove migrations

---

## ✅ Testing Checklist

After integration:

- [ ] Add news in admin portal → appears on news page
- [ ] Upload gallery image → appears in gallery
- [ ] Add teacher profile → appears on staff page
- [ ] Create event → appears on events calendar
- [ ] Upload file → appears in downloads
- [ ] Edit content → changes reflect immediately
- [ ] Delete content → removed from public pages
- [ ] Unpublish content → hidden from public (still in admin)

---

## 🎯 Quick Test

1. Go to `/admin/`
2. Add a news article with image
3. Mark as "Published"
4. Save
5. Go to your news page
6. **If integrated:** You'll see the new article
7. **If not integrated yet:** Won't appear (but it's saved in database!)

---

## 💡 Pro Tips

1. **Always filter by `published=True`** in public views
2. **Use `order_by()` for consistent ordering**
3. **Add pagination** for long lists:
   ```python
   from django.core.paginator import Paginator
   
   paginator = Paginator(news, 10)  # 10 per page
   page = paginator.get_page(request.GET.get('page'))
   ```

4. **Handle missing images gracefully**:
   ```html
   {% if news.image %}
       <img src="{{ news.image.url }}">
   {% else %}
       <img src="{% static 'images/default-news.jpg' %}">
   {% endif %}
   ```

5. **Use select_related** for performance:
   ```python
   NewsAnnouncement.objects.filter(
       published=True
   ).select_related('created_by').order_by('-created_at')
   ```

---

## 🚀 Next Steps

1. **Integrate one page at a time** (start with news)
2. **Test each integration** before moving to next
3. **Update templates** to use new model fields
4. **Migrate existing data** if needed
5. **Remove old system** once everything works

Need help integrating specific pages? Let me know!
