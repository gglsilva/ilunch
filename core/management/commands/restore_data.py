import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.dateparse import parse_datetime, parse_date
import re
import os

from account.models import Profile
from product.models import Product, Category
from order.models import Order, OrderItem


class Command(BaseCommand):

    def restore_profiles(self):
        # Caminho do arquivo CSV
        csv_file_path = os.path.join(settings.BASE_DIR, 'core/management/commands/active_profiles.csv')

        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row.get('username')
                first_name = row.get('first_name', '')
                last_name = row.get('last_name', '')
                email = row.get('email', '')
                date_of_birth = row.get('date_of_birth', None)

                if not User.objects.filter(username=username).exists():
                    new_user = User()
                    new_user.username=username
                    new_user.first_name=first_name
                    new_user.last_name=last_name
                    new_user.email=email
                    new_user.set_password('adminadmin')
                    new_user.save()
                    
                    profile = Profile.objects.create(user=new_user)
                    if date_of_birth:
                        # Supondo que você tenha um perfil de usuário onde a data de nascimento é armazenada
                        profile.date_of_birth = date_of_birth
                        profile.save()

                    self.stdout.write(self.style.SUCCESS(f'Usuário {username} criado com sucesso.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Usuário {username} já existe no sistema.'))
                    
    def restore_products(self):
        # Abra o arquivo CSV
        csv_file_path = os.path.join(settings.BASE_DIR, 'core/management/commands/products.csv')
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Verifica se a categoria existe, senão cria
                category, _ = Category.objects.get_or_create(
                    name=row['category'],
                    slug=row['category'].lower().replace(" ", "-")
                )

                # Cria ou atualiza o produto no banco de dados
                product, created = Product.objects.update_or_create(
                    slug=row['slug'],
                    defaults={
                        'category': category,
                        'name': row['name'],
                        'image': row['image'] if row['image'] else None,
                        'description': row['description'] if row['description'] else '',
                        'price': row['price'] if row['price'] else None,
                        'available': row['available'].lower() == 'true',
                        'created': parse_datetime(row['created']),
                        'updated': parse_datetime(row['updated']),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Produto '{product.name}' criado."))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Produto '{product.name}' atualizado."))

    def restore_orders(self):
        
        csv_file_path = os.path.join(settings.BASE_DIR, 'core/management/commands/orders.csv')

        # Abra o arquivo CSV
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Verifica se o cliente existe
                try:
                    client = Profile.objects.get(user__username=row['client_name'])
                except Profile.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Cliente '{row['client_name']}' não encontrado."))
                    continue

                # Cria o pedido
                order = Order.objects.create(
                    client=client,
                    note=row['note'] if row['note'] else '',
                    status=Order.CREATED,
                    created=parse_date(row['created'])
                )

                # Processa os produtos
                products = row['products']
                product_entries = re.findall(r'(\w+\s*\w*)\s*\(x(\d+)\)', products)

                for product_name, quantity in product_entries:
                    try:
                        product = Product.objects.get(name=product_name.strip())
                    except Product.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Produto '{product_name}' não encontrado."))
                        continue

                    # Cria o item do pedido
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=int(quantity)
                    )

                self.stdout.write(self.style.SUCCESS(f"Pedido '{order.id}' criado para o cliente '{client.user.username}'."))

        
    def handle(self, *args, **options):
        
        self.restore_profiles()
        
        # self.restore_orders()
        # self.restore_products()
        self.restore_orders()
