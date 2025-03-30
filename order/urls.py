from django.urls import path
from . import views

app_name='order'

urlpatterns = [
    path('create/', views.action_fetch_create_order, name="action_fetch_create_order"),
    path('edit/', views.order_edit, name="order_edit"),
    path('print/orders/', views.print_report_orders, name="print_report_orders"),
    path('print/orders/week', views.print_weekly_report, name="print_weekly_report"),
    path('orders-today/', views.get_orders_today, name='get_orders_today'),
    path("orders-by-period/", views.get_orders_by_period, name="orders_by_period"),
    path("print-orders/", views.print_orders_pdf, name="print_orders"),
]