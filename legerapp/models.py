from django.db import models

# Create your models here.
class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    updated_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True)

class Carousel(models.Model):
    image_name = models.CharField(max_length=255)
    image_title = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255)
    product_price = models.IntegerField()
    product_discount = models.IntegerField(null=True)
    description = models.TextField(null=True)
    product_image = models.ImageField(null=True, upload_to='product_images/')
    items_available = models.IntegerField()
    size = models.CharField(max_length=100)
    
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    
class About(models.Model):
    about = models.TextField()