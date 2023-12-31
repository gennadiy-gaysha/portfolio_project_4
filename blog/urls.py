from django.urls import path
from blog import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetails.as_view(),
         name='post-details'),
    path('create_post/', views.CreatePost.as_view(),
         name='create-post'),
    path('update_post/<slug:slug>/', views.UpdatePost.as_view(),
         name='update-post'),
    path('delete_post/<slug:slug>/', views.DeletePost.as_view(),
         name='delete-post'),
    path('search_country/', views.search_country,
         name='search-country'),
    path('like/<slug:slug>/', views.PostLike.as_view(),
         name='post-like'),
    path('<slug:slug>/', views.ShowCountry.as_view(),
         name='show-country'),
    path('draft_list/<str:username>/', views.DraftList.as_view(),
         name='draft-list'),
    path('published_list/<str:username>/', views.PublishedList.as_view(),
         name='published-list'),
    path('moderation_list/<str:username>/', views.ModerationList.as_view(),
         name='moderation-list'),
]
