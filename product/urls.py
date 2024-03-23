from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('create/', views.product_create, name='product_create'),
    path('list/', views.product_list, name='product_list'),
    path('update/', views.product_update, name='product_update'),
    path('remove/', views.product_remove, name='product_remove'),
]   
