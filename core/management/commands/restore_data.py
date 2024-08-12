import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from account.models import Profile


class Command(BaseCommand):

    def restore_profiles(self):
        # Caminho do arquivo CSV
        csv_file_path = '/home/gabriel/Documentos/Python/Projetos/ilunch/core/management/commands/active_profiles.csv'

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
                    
    
    def restore_orders(self):
        
        csv_file_path = '/home/gabriel/Documentos/Python/Projetos/ilunch/core/management/commands/orders.csv'
        
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                client = row.get('client_name')
                note = row.get('note', '')
                created = row.get('created', '')
                products = row.get('products', '')
                
                print('cliente:', client)
                print('products', products.split(' (x1),'))

        
    def handle(self, *args, **options):
        
        # self.restore_profile()
        
        self.restore_orders()