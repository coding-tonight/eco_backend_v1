from django.db import models

from app.models import Base

# Create your models here.

class Category(Base):
    category_name = models.CharField(max_length=45)
    icon_url = models.ImageField(upload_to='uploads/category/icons/',null=True, blank=True)

    class Meta:
        db_table = 'category'

