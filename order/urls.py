from django.urls import path
from . import views

app_name='order'

urlpatterns = [
    path('create/', views.action_fetch_create_order, name="action_fetch_create_order"),
    path('edit/', views.order_edit, name="order_edit"),
    path('print/orders/', views.print_report_orders, name="print_report_orders"),
    path('print/orders/week', views.print_weekly_report, name="print_weekly_report")
]