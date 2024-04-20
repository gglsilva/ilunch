from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(
        verbose_name='Nome',
        max_length=60,
        blank=False,
        null=False,
    )
    cnpj = models.CharField(
        verbose_name='CNPJ',
        max_length=14,
        blank=True,
        null=True,
    )
    phone = models.CharField(
        verbose_name='Telefone',
        max_length=14,
        blank=True,
        null=True,
    )
    max_time_order = models.TimeField(
        verbose_name='Horário máximo para fazer o pedido',
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name='Restaurante esta ativo',
        default=False
    )
    
    def __str__(self):
        return self.name
