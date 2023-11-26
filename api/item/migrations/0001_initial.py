# Generated by Django 4.2.6 on 2023-11-26 13:21

import uuid 

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0003_alter_category_reference_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(default=uuid.uuid4().hex, max_length=32, unique=True)),
                ('color_name', models.CharField(max_length=10, null=True)),
                ('color_code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'colors',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(default=uuid.uuid4().hex, max_length=32, unique=True)),
                ('tilte', models.CharField(max_length=45)),
                ('desc', models.TextField(blank=True, max_length=200, null=True)),
                ('percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('color', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'discount',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(default=uuid.uuid4().hex, max_length=32, unique=True)),
                ('product_name', models.CharField(max_length=200)),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='item.discount')),
                ('slug', models.SlugField(unique=True)),
                ('thumbnail', models.ImageField(upload_to='uploads/product/')),
                ('featured', models.BooleanField(default=False)),
                ('recommeded', models.BooleanField(default=False)),
                ('categroy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='category.category')),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'product',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(default=uuid.uuid4().hex, max_length=32, unique=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='item.product')),
                ('qty', models.IntegerField()),
                ('color', models.ManyToManyField(related_name='+', to='item.color')),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'product_variant',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(default=uuid.uuid4().hex, max_length=32, unique=True)),
                ('size', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'sizes',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(default=uuid.uuid4().hex, max_length=32, unique=True)),
                ('sku_code', models.CharField(max_length=20)),
                ('varinat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='item.productvariant')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='item.size')),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(default=uuid.uuid4().hex, max_length=32, unique=True)),
                ('title', models.CharField(max_length=45)),
                ('slug', models.SlugField()),
                ('product', models.ManyToManyField(blank=True, related_name='+', to='item.product')),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tags',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='SkuImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(default=uuid.uuid4().hex, max_length=32, unique=True)),
                ('image_path', models.ImageField(upload_to='uploads/sku/')),
                ('image_name', models.CharField(max_length=45)),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='item.sku')),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]