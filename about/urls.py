from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.display_last_about, name='about')
]
