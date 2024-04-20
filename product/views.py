from django.shortcuts import render
from .models import Category, Product
from account.models import Profile
from restaurant.models import Restaurant
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


# Create your views here.
def product_create(request):
    pass


@login_required
def product_list(request, category_slug=None):
    # Verifica se o horário máximo para fazer o pedido foi atingido
    restaurant = Restaurant.objects.filter(is_active=True).first()
    if restaurant and restaurant.max_time_order:
        current_datetime = timezone.now()
        new_datetime = current_datetime - timedelta(hours=3)
        current_time = new_datetime.time()
        # print(f"current_time:{current_time}; restaurant.max_time_order{restaurant.max_time_order}")
        if current_time > restaurant.max_time_order:
            response = {
                'warning': 'Os pedidos foram encerrados. Por favor, entre em contato com o restaurante.'
            }
            return JsonResponse(response, safe=False)
            # return JsonResponse({'response': 'error', 'message': 'Os pedidos foram encerrados. Por favor, entre em contato com o restaurante.'}, status=400)
    
    categories = Category.objects.all()
    acompanhamento = Product.objects.filter(
        available=True, category=categories[0])
    opcao = Product.objects.filter(available=True, category=categories[1])
    profiles = Profile.objects.filter(is_active=True)

    html = render_to_string(
        template_name='product/product_list.html',
        context={
            'opcoes': opcao,
            'acompanhamentos': acompanhamento,
            'profiles': profiles,
        },
        request=request
    )

    response = {'data': html}
    return JsonResponse(response, safe=False)


def product_update(request):
    pass


def product_remove(request):
    pass


def product_list_menu(request):
    company = Company.objects.filter(active=True)

    menu = Menu.objects.filter(campany=company)
