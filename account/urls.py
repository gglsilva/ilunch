from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('register/done/', views.register_done, name='register_done'),
    path('edit/', views.edit, name='edit'),
]
