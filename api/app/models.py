import uuid

from django.db import models
from django.contrib.auth.models import User



def uuid_generator():
    return uuid.uuid4().hex


# Create your models here.

class Base(models.Model):
    reference_id = models.CharField(max_length=32,unique=True, default=uuid_generator())
    created_by  = models.DateTimeField(auto_now=False)
    created_at = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT ,db_column="created_at")
    updated_at = models.DateTimeField(null=True, auto_now=False)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT, db_column="updated_by", null=True)

    class Meta:
        abstract = True

class OTP(models.Model):
    user = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE, db_column='user')
    email = models.EmailField(max_length=45)
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = 'otp'
    
    def __str__(self):
        return self.email
