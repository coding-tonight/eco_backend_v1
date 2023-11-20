from django.db import models

from app.models import Base
from category.models import Category

# Create your models here.


class Size(Base):
    size = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.size

    class Meta:
        db_table = 'size'
        ordering = ('created_at')

class Color(Base):
    color_code = models.CharField(max_length=10, unique=True)
    color_name  = models.CharField(max_length=10)

    def __str__(self):
        return self.color_name
    
    class Meta:
        db_table = 'color'
        ordering = ('created_at')


class Item(Base):
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, related_name="+", on_delete=models.PROTECT, db_column='category')
    thumbnail = models.ImageField(upload_to='uploads/products/', null=False, blank=True)
    slug = models.SlugField(max_length=225)
    
    def __str__(self):
        return self.item_name
    
    class Meta:
        db_table = 'items'
        ordering = ('created_at')
    

class Discount(Base):
    name = models.CharField(max_length=45)
    desc = models.CharField(max_length=60, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=3, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'discounts'
        ordering = ('created_at')


class ItemDetail(Base):
    item_id = models.OneToOneField(Item, related_name="+", on_delete=models.CASCADE, db_column="item_id")
    size_id = models.ManyToManyField(Size, related_name="+" ,on_delete=models.PROTECT, db_column="item_id",through="Size")
    item_colors = models.ManyToManyField()
    item_desc = models.TextField(max_length=200, null=True, blank=True)
    item_rating = models.IntegerField(max=5, null=True)
    tiktok = models.URLField(max_length=255)
    discount_id = models.ForeignKey(Discount, related_name="+", on_delete=models.PROTECT, db_column='discount_id')

    class Meta:
        db_table = 'itemDetails'

