from django.urls import path
from blog import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetails.as_view(), name='post-details'),
    path('create_post/', views.CreatePost.as_view(), name='create-post')
]