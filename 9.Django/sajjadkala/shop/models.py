from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    PRODUCT_CATEGORY = [
        ('Food', 'مواد غذایی'),
        ('Clothing', 'پوشاک'),
        ('Electronics', 'لوازم الکترونیکی'),
        ('Furniture', 'اثاثیه منزل'),
        ('Other', 'سایر')
    ]
    
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    description = models.TextField()
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=PRODUCT_CATEGORY)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.product.name}"

class Rate:
    pass

class Order:
    pass

class Cart:
    pass
