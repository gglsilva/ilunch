from django.db import models
from django.utils.text import slugify
from product.models import Category, Product
from core.models import Active, TimeStampedModel

# Create your models here.
class Company(TimeStampedModel, Active):
    name = models.CharField(
        'Nome Fantasia', 
        max_length=100
    )
    cnpj = models.CharField(
        'Nome',
        max_length=18
    )
    address = models.CharField(
        'Endereço',
        max_length=200
    )
    phone = models.CharField(
        'Telefone',
        max_length=15
    )
    email = models.EmailField()
    site = models.CharField(
        'Site',
        max_length=80
    )

    def __str__(self):
        return str(self.name)


class Menu(TimeStampedModel, Active):
    name = models.CharField(
        'Nome', 
        max_length=100
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    description = models.TextField(
        'Descrição',
        blank=True
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        verbose_name="slug",
        help_text="Preenchido automaticamente, não editar",
        null=True, 
        blank=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    @property
    def get_product_for_order(self):
        return ''.join(f'{item.product.name}, ' for item in self.menu_product.all())    
# class MenuCategory(TimeStampedModel, Active):
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     order = models.PositiveIntegerField('ordem')

#     def __str__(self):
#         return str(self.category.name + ' - ' + self.menu.name)

#     class Meta:
#         ordering = ('order',)
#         unique_together = [("menu", "category")]


class MenuItem(TimeStampedModel, Active):
    menu = models.ForeignKey(
        Menu,
        related_name='menu_itens',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='menu_product',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        'Valor',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    def __str__(self):
        return str(self.id)