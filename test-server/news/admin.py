from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    # Columns displayed in the admin list view
    list_display = ('title', 'created_at', 'updated_at')
    
    # Adds a search bar targeting these specific fields
    search_fields = ('title', 'content')
    
    # Adds a filter sidebar on the right side for dates
    list_filter = ('created_at',)
    
    # Sorts announcements by newest first by default
    ordering = ('-created_at',)