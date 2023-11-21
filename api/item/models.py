from django.db import models
from django.urls import reverse

from app.models import Base
from category.models import Category

# Create your models here.

""" model managers section
"""
class ItemVariantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)
    
    def color(self):
        pass

    def size(self):
        pass



class Discount(Base):
    tilte = models.CharField(max_length=45)
    desc = models.TextField(max_length=200, null=True, blank=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.tilte
    
    class Meta:
        db_table = 'discount'
        ordering = ('created_at')


class Size(Base):
    size = models.CharField(max_length=5)

    def __str__(self):
        return self.size
    
    class Meta:
        db_table = 'sizes'
        ordering = ('created_at')


class Color(Base):
    color_name = models.CharField(max_length=10, null=True)
    color_code = models.CharField(max_length=10, blank=False)
    
    def __str__(self):
        return self.color_name
    
    class Meta:
        db_table = 'colors'
        ordering = ('created_at')


class Item(Base):
    item_code = models.CharField(max_length=45)
    item_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, related_name="+", on_delete=models.PROTECT)
    thumbnail = models.ImageField(upload_to='uploads/product/thumbnail/', null=True)

    def __str__(self):
        return self.item_name
    
    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})  

    class Meta:
        db_table = 'items'
        ordering = ('created_at')


class ItemVariant(Base):
    item = models.ForeignKey(Item, related_name="+", on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_length=10, decimal_places=2)
    size = models.ForeignKey(Size, related_name="+", on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name="+", on_delete=models.PROTECT)
    stock = models.IntegerField(max_length=10, null=True)

    def __str__(self):
        return f"variant of {self.item.item_name}"

    class Meta:
        db_table = 'item_variant'
        ordering = ('created_at')

