from django.urls import path
from . import views

app_name='core'

urlpatterns = [
    path('memory/', views.memory_game, name="memory")
]
