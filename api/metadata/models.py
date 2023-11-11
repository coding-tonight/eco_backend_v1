from django.db import models

from app.models import Base

# Create your models here.


class MetaData(Base):
    app_name = models.CharField(max_length=45)
    contact_number = models.CharField(max_length=14)
    address = models.CharField(max_length=20)
    logo = models.ImageField(null=False, blank=False, upload_to='uploads/metadata/')

    class Meta:
        db_table = 'metaData'
    
    def __str__(self):
        return self.app_name
    
    