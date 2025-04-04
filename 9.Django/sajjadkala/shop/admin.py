from django.contrib import admin
from .models import *
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'price', 'category']


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
