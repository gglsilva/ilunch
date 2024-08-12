import os
import csv
from datetime import datetime
import django

# Configurar o Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ilunch.settings')
django.setup()

from django.contrib.auth import get_user_model
from account.models import Profile

def populate_profiles_from_csv(file_path):
    User = get_user_model()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row['username']
            first_name = row['first_name']
            last_name = row['last_name']
            email = row['email']
            date_of_birth = row['date_of_birth']
            
            if date_of_birth:
                date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            else:
                date_of_birth = None

            # Cria um usuário ou atualiza se o usuário já existir
            user, created = User.objects.update_or_create(
                username=username,
                defaults={
                    'first_name': first_name or '',
                    'last_name': last_name or '',
                    'email': email or '',
                    'password': 'password123',  # Defina uma senha padrão ou ajuste conforme necessário
                }
            )

            # Cria um perfil ativo para o usuário
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'date_of_birth': date_of_birth,
                    'photo': '',  # você pode ajustar isso para apontar para uma imagem de placeholder
                    'is_active': True
                }
            )

if __name__ == '__main__':
    file_path = os.path.join(os.path.dirname(__file__), 'active_profiles.csv')  # Caminho para o seu arquivo CSV na raiz do projeto
    populate_profiles_from_csv(file_path)
    print('Successfully populated the database with active profiles from CSV')