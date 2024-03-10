from django.db import models
from django.conf import settings

class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(
        'Data de nascimento',
        blank=True,
        null=True
    )
    photo = models.ImageField(
        'Foto',
        upload_to='users/%Y/%m/%d/',
        blank=True
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True
    )
    
    def __str__(self):
        return f'{self.user.username}'
    