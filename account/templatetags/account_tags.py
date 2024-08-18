from django import template
from order.models import Order
from restaurant.models import Restaurant
from datetime import datetime, date, timedelta
import re

register = template.Library()

@register.simple_tag
def total_order(user):
    return Order.objects.filter(client=user).count()

@register.simple_tag
def total_order_today(user):
    return Order.objects.filter(client=user, created=date.today()).count()

@register.simple_tag
def total_mean_order(user):
    return Order.objects.filter(client=user, created__gte=date.today() - timedelta(days=5)).count()

@register.simple_tag
def max_time_order():
    max_time = Restaurant.objects.filter(is_active=True).first()
    if max_time and max_time.max_time_order:
        # Converte max_time_order para datetime combinando com uma data qualquer (por exemplo, 1 de janeiro de 1900)
        datetime_obj = datetime.combine(datetime.min, max_time.max_time_order)
        # Subtrai 3 horas
        new_time = (datetime_obj - timedelta(hours=3)).time()
        return new_time.strftime('%H:%M')
    return ""

@register.simple_tag
def contact_restaurant():
    if (
        phone_number := Restaurant.objects.filter(is_active=True)
        .values_list('phone', flat=True)
        .first()
    ):
        # Remove todos os caracteres não numéricos do número de telefone
        digits = re.sub(r'\D', '', phone_number)
        # Formata o número de telefone no formato desejado
        return f"({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}"
    else:
        return "N/A"