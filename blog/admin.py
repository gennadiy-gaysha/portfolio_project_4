from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Country, Post, Comment


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['country_name']}
    search_fields = ['country_name']


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'status', 'created_on']
    list_filter = ['status', 'created_on']
    search_fields = ['title', 'content']
    ordering = ['-created_on']
    summernote_fields = ['content']
    actions = ['approve_posts']

    def approve_posts(self, queryset):
        """
        Updates the status of the selected posts in the queryset
        to a value of 2, indicating that they have been approved.
        """
        queryset.update(status=2)

    approve_posts.short_description = 'Approve posts'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'body', 'post', 'created_on', 'approved']
    list_filter = ['approved', 'created_on']
    search_fields = ['name', 'email', 'address', 'body']
    actions = ['approve_comments']

    def approve_comments(self, queryset):
        """
        Updates the status of the selected comments in the queryset
        to a value of True, indicating that they have been approved.
        """
        queryset.update(approved=True)

    approve_comments.short_description = 'Approve comments'
