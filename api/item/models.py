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

class Discount(Base):
    tilte = models.CharField(max_length=45)
    desc = models.TextField(max_length=200, null=True, blank=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.tilte

    class Meta:
        db_table = 'discount'
        ordering = ['created_at']


class Size(Base):
    size = models.CharField(max_length=5)

    def __str__(self):
        return self.size

    class Meta:
        db_table = 'sizes'
        ordering = ['created_at']


class Color(Base):
    color_name = models.CharField(max_length=10, null=True)
    color_code = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.color_name

    class Meta:
        db_table = 'colors'
        ordering = ['created_at']


class Product(Base):
    product_name = models.CharField(max_length=200)
    categroy = models.ForeignKey(Category, related_name="+", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    discount = models.ForeignKey(
        Discount, related_name="+", on_delete=models.PROTECT)
    thumbnail = models.ImageField(upload_to='uploads/product/')
    featured = models.BooleanField(default=False)
    recommeded = models.BooleanField(default=False)

    objects = ItemVariantManager()
    product = models.Manager()

    def get_absolute_url(self):
        return reverse('product:detali', kwargs={'slug': self.slug})

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'product'
        ordering = ['created_at']


class ProductVariant(Base):
    product = models.ForeignKey(
        Product, related_name="+", on_delete=models.CASCADE)
    color = models.ManyToManyField(
        Color, related_name="+")
    qty = models.IntegerField()

    class Meta:
        db_table = 'product_variant'
        ordering = ['created_at']


class Sku(Base):
    varinat = models.ForeignKey(
        ProductVariant, related_name="+", on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name="+", on_delete=models.PROTECT)
    sku_code = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.varinat.product.product_name


class SkuImage(Base):
    sku = models.ForeignKey(Sku , related_name="+", on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='uploads/sku/')
    image_name = models.CharField(max_length=45)

    def __str__(self):
        return self.image_name

class Tags(Base):
    title = models.CharField(max_length=45)
    slug = models.SlugField()
    product = models.ManyToManyField(Product, related_name="+" , blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tags'
        ordering = ['created_at']

    