from django.contrib import admin
from .models import Category, Product, Menu


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['category','available', 'created', 'updated']
    list_editable = ['price', 'available']
    search_fields = ['name', 'created', 'price']
    prepopulated_fields = {'slug': ('name',)}
    
admin.site.register(Menu)