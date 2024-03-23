from django.shortcuts import render
from .models import Category, Product
from account.models import Profile
from menu.models import Company, Menu, MenuItem
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


# Create your views here.
def product_create(request):
    pass


@login_required
def product_list(request, category_slug=None):

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
