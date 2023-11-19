from django.db import models

from app.models import Base
from category.models import Category

# Create your models here.


class Item(Base):
    item_name = models.CharField(max_length=45)
    item_price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, related_name="+", on_delete=models.PROTECT, db_column='category')

    class Meta:
        db_table = 'items'

class Discount(Base):
    name = models.CharField(max_length=45)
    desc = models.CharField(max_length=60, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=3, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'discounts'


class ItemDetail(Base):
    item_id = models.OneToOneField(Item, related_name="+", on_delete=models.CASCADE, db_column="item_id")
    item_size = models.Choices()
    item_colors = models.CharField()
    item_desc = models.TextField(max_length=200, null=True, blank=True)
    discount_id = models.ForeignKey(Discount, related_name="+", on_delete=models.PROTECT, db_column='discount_id')

    class Meta:
        db_table = 'itemDetails'

