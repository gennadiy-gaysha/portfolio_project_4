from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.RegisterNewAccount.as_view(), name='register'),
    path('edit_details/', views.EditDetails.as_view(), name='edit-details')
]