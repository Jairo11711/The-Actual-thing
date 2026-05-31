from django.shortcuts import render
from .models import Announcement

# Create your views here.
def index(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    
    context = {
        'announcements': announcements
    }
    return render(request, 'news/news_page.html', context)
