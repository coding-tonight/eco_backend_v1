from django.db import models
from django.db.models.query import QuerySet
from django.utils.text import slugify

from app.models import Base
from category.models import Category

# Create your models here.


class Size(Base):
    size_code = models.CharField(max_length=10)  # xl | xxl | sm  example
    size = models.CharField()  # small , extra large , double xl

    def __str__(self):
        return self.size_code

    class Meta:
        db_table = 'sizes'
        ordering = ['created_at']


class Color(Base):
    color_name = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=15)

    def __str__(self):
        return self.color_name

    class Meta:
        ordering = ['created_at']
        db_table = 'colors'


""" product models section.
"""

class ProductQuerySet(models.QuerySet):

    def get_deleted_product(self):
        return self.filter(is_delete=True)
    
    def get_all_product(self):   # excludes the deleted items
        return self.filter(is_delete=False)


class ProductManager(models.Manager):
    """ product manager 
    """
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def get_all_product(self):
        return ProductQuerySet.get_all_product()
    
    def delete_product(self):
        return ProductQuerySet.get_deleted_product()
    


class Product(Base):
    product_name = models.CharField(max_length=45)
    product_code = models.CharField(max_length=15)
    description = models.TextField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name="+", on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    is_recommeded = models.BooleanField(default=False)
    thumbnail = models.ImageField(
        upload_to='uploads/product/thumbnail/', blank=True, null=True)
    slug = models.SlugField(unique=True)


    objects = models.Manager()
    product_objects = ProductManager()

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return slugify(f"{self.category.category_name} {self.product_name}")

    class Meta:
        db_table = 'product'
        ordering = ['created_at']


class ProductVariant(Base):
    product = models.ForeignKey(
        Product, related_name="+", on_delete=models.CASCADE)
    price = models.DecimalField()
    color = models.ManyToManyField(
        Color, related_name="+", on_delete=models.PROTECT)
    size = models.ManyToManyField(
        Size, related_name="+", on_delete=models.PROTECT)
    stock = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'product_attributes'
        ordering = ['created_at']


class ProductImage(Base):
    variant = models.ForeignKey(
        ProductVariant, related_name="+", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product/image', null=True)


    def __str__(self):
        return f"{self.variant.product.product_name}-{self.reference_id}"

    class Meta: 
        db_table = 'product_image'

