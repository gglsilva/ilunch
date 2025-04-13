from account.models import Profile
from order.models import Order, OrderItem
from product.models import Product, Category
from restaurant.models import Restaurant
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Count, Sum
from datetime import date, timedelta, datetime
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import json
import locale

# Defina o locale para português se quiser o nome dos dias em PT
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")  # pode variar por SO


def action_fetch_create_order(request):
    
    if request.method != 'POST':
        return JsonResponse({'response': 'error', 'message': 'Método inválido. Apenas requisições POST são permitidas.'}, status=400)    
    
    data = json.loads(request.body)
    order_edit = data.get('order_number')
    produtos = data.get('produtos')
    cliente = data.get('cliente')
    mensagem = data.get('msg')
    profile = Profile.objects.get(user__username=cliente)

    if order_edit != None:
        
        order = Order.objects.get(id=int(order_edit))
        order.items.all().delete()
        order.note = mensagem
        order.save()
        
        for item in produtos:
            produto = Product.objects.get(id=int(item))
            OrderItem.objects.create(order=order,
                                    product=produto,
                                    )

        return JsonResponse({'response': 'success'})
    else:          
        # Verifica se o restaurante está aceitando pedidos no momento
        restaurant = Restaurant.objects.get(is_active=True)
        current_time = timezone.now().time()
        
        if restaurant.max_time_order and current_time > restaurant.max_time_order:
            return JsonResponse({'response': 'error', 'message': 'Os pedidos foram encerrados. Por favor, entre em contato com o restaurante.'}, status=400)
        
        order = Order.objects.create(client=profile, note=mensagem, created=timezone.now())
        for item in produtos:
            produto = Product.objects.get(id=int(item))
            OrderItem.objects.create(order=order,
                                    product=produto,
                                    )

        return JsonResponse({'response': 'success'})


def order_edit(request):
    user = request.user
    today = date.today()

    last_order = Order.objects.filter(
        client=user.profile,
        created=today
    ).order_by('-id').first()
    
    if last_order is None:
        response = {
            'warning': 'É necessário fazer um pedido antes, para poder editá-lo.'
        }
        return JsonResponse(response, safe=False)

    categories = Category.objects.all()
    acompanhamento = Product.objects.filter(available=True, category=categories[0])
    opcao = Product.objects.filter(available=True, category=categories[1])
    profiles = Profile.objects.filter(is_active=True)

    order_itens = last_order.items.all()
    order_number = last_order.id

    list_last_product_select = [item.product.name for item in order_itens]
    html = render_to_string(
        template_name='product/product_list.html',
        context={
            'opcoes': opcao,
            'acompanhamentos': acompanhamento,
            'profiles': profiles,
            'order_number': order_number,
            # 'last_order':list_last_product_select,
            'last_order':last_order,
            'note': last_order.note

        },  
        request=request
    )

    response = {
                    'data':html, 
                }

    return JsonResponse(response, safe=False)

def print_report_orders(request):
    today = date.today()
    orders = Order.objects.filter(created=date.today())
    html_string = render_to_string(
                            'order/pdf.html', 
                                {
                                    'orders': orders,
                                    'today': today
                                }
                            )

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/pedidos.pdf')

    fs = FileSystemStorage('/tmp')

    with fs.open('pedidos.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'
    return response


def print_weekly_report(request):
    # Calcula a data de uma semana atrás
    one_week_ago = date.today() - timedelta(days=7)
    # Filtra os pedidos criados na última semana, de segunda a sexta
    orders = Order.objects.filter(created__gte=one_week_ago, created__week_day__range=(2, 6))

    # Conta a quantidade de pedidos por dia da semana
    order_counts = {}
    total_orders = 0
    for order in orders:
        day = order.created
        if day in order_counts:
            order_counts[day]['count'] += 1
        else:
            order_counts[day] = {
                'day_name': day.strftime('%A'),
                'count': 1
            }
        total_orders += 1

    # Ordena por data
    ordered_counts = sorted(order_counts.items())

    # Gera o HTML a partir do template
    html_string = render_to_string(
        'order/weekly_report.html',
        {
            'order_counts': ordered_counts,
            'total_orders': total_orders,
            'today': date.today(),
        }
    )

    # Converte o HTML para PDF
    html = HTML(string=html_string)
    pdf_path = '/tmp/pedidos_semana.pdf'
    html.write_pdf(target=pdf_path)

    # Salva o PDF no sistema de arquivos e prepara a resposta HTTP
    fs = FileSystemStorage('/tmp')
    with fs.open('pedidos_semana.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pedidos_semana.pdf"'
    
    return response
            
            
def get_orders_today(request):
    today = date.today()
    orders = Order.objects.filter(created=today).values(
        'id', 'client__user__username', 'created'
    )
    return JsonResponse({'orders': list(orders)})


# def get_orders_by_period(request):
#     start_date = request.GET.get("start_date")
#     end_date = request.GET.get("end_date")

#     if not start_date or not end_date:
#         return JsonResponse({"error": "Datas inválidas"}, status=400)

#     start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#     end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

#     # Agrupar pedidos pela data e contar quantos existem em cada dia
#     orders_by_date = (
#         Order.objects
#         .filter(created__range=[start_date, end_date])
#         .values("created")  # Agrupar pela data de criação
#         .annotate(count=Count("id"))  # Contar os pedidos por data
#         .order_by("-created")  # Ordenar pela data
#     )

#     # Formatar a data antes de enviar ao frontend
#     formatted_orders = [
#         {"created": order["created"].strftime("%d/%m/%Y"), "count": order["count"]}
#         for order in orders_by_date
#     ]

#     return JsonResponse({"orders": formatted_orders})
def get_orders_by_period(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if not start_date or not end_date:
        return JsonResponse({"error": "Datas inválidas"}, status=400)

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    orders_by_date = (
        Order.objects
        .filter(created__range=[start_date, end_date])
        .values("created")  # já é um DateField, então pode agrupar direto
        .annotate(count=Count("id"))
        .order_by("-created")
    )

    formatted_orders = [
        {"created": order["created"].strftime("%d/%m/%Y"), "count": order["count"]}
        for order in orders_by_date
    ]

    total_orders = sum(order["count"] for order in formatted_orders)

    return JsonResponse({
        "orders": formatted_orders,
        "total": total_orders
    })


def print_orders_pdf(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if not start_date or not end_date:
        return HttpResponse("Datas inválidas", status=400)

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    orders = Order.objects.filter(created__range=[start_date, end_date])

    # Gera o HTML do relatório
    html_string = render_to_string(
        "order/period_report.html",
        {"orders": orders, "start_date": start_date, "end_date": end_date}
    )

    # Converte o HTML para PDF
    html = HTML(string=html_string)
    pdf_path = "/tmp/pedidos_periodo.pdf"
    html.write_pdf(target=pdf_path)

    # Retorna o PDF como resposta
    fs = FileSystemStorage("/tmp")
    with fs.open("pedidos_periodo.pdf") as pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="pedidos_periodo.pdf"'
        return response