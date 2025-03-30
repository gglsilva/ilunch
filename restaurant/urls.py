from django.urls import path
from .views import restaurant_list, restaurant_detail, restaurant_update

app_name='restaurant' 

urlpatterns = [
    path('restaurants/list/', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
    path('restaurants/<int:restaurant_id>/update/', restaurant_update, name='restaurant_update'),
]
