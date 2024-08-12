from django import template
from order.models import Order
from restaurant.models import Restaurant
from datetime import date, timedelta
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
    return max_time.max_time_order.strftime('%H:%M') if max_time else ""
    

@register.simple_tag
def contact_restaurant():
    phone_number = Restaurant.objects.filter(is_active=True).values_list('phone', flat=True).first()
    if phone_number:
        # Remove todos os caracteres não numéricos do número de telefone
        digits = re.sub(r'\D', '', phone_number)
        # Formata o número de telefone no formato desejado
        formatted_phone_number = "({}) {} {}-{}".format(
            digits[:2], digits[2], digits[3:7], digits[7:]
        )
    else:
        formatted_phone_number = "N/A"  # ou qualquer outra mensagem que deseje exibir se não houver número de telefone definido
    return formatted_phone_number