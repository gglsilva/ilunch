from django.contrib import admin
from .models import Menu, MenuItem, Company


# Register your models here.
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    raw_id_fields = ['product']

# class MenuCategoryInLine(admin.StackedInline):
#     model = MenuCategory
#     extra = 1


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        # MenuCategoryInLine,
        MenuItemInline,
    ]

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Menu, MenuAdmin)
admin.site.register(Company, CompanyAdmin)