from django.db import models
from django.urls import reverse
from restaurant.models import Restaurant


class Category(models.Model):
    name = models.CharField(
        'Categoria',
        max_length=200,
        db_index=True
    )
    slug = models.SlugField(
        'Slug',
        max_length=200,
        unique=True
    )


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

    
    
class Product(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='produtos'
    )
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        'Nome do produto',
        max_length=200,
        db_index=True
    )
    slug = models.SlugField(
        'Slug',
        max_length=200,
        unique=True
    )
    image = models.ImageField(
        'Imagem',
        upload_to='products/%Y/%m/%d',
        blank=True        
    )
    description = models.TextField(
        'descrição',
        blank=True
    )
    price = models.DecimalField(
        'Valor',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    products = models.ManyToManyField(
        'self', 
        blank=True, 
        symmetrical=False, 
        related_name='combos'
    )
    available = models.BooleanField(
        'Ativo',
        default=True
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


class Menu(models.Model):
    name = models.CharField(
        verbose_name='Nome',
        max_length=60,
        blank=False,
        null=False,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE, 
        related_name='menus'
    )
    product = models.ManyToManyField(
        Product, 
        verbose_name="Produtos",
        related_name='menus',
    )
    
    def __str__(self):
        return self.name