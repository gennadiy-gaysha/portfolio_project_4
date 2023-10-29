from django.contrib import admin
from .models import About
from django_summernote.admin import SummernoteModelAdmin

@admin.register(About)
class PostAdmin(SummernoteModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title', 'content']
    summernote_fields = ['content']
