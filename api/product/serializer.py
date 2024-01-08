from django.db import transaction

from rest_framework import serializers
from product.models import Size, Color, Discount, Product, ProductVariant

from category.serializer import CategorySerializer
from category.models import Category
from product.models import ProductImage, Product, ProductVariant, Tags


class SizeSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    size_code = serializers.CharField()
    size = serializers.CharField()

    def validate_size_code(self, value):
        if not value:
            raise serializers.ValidationError('size code field is required.')

        return value

    def validate_size(self, value):
        if not value:
            raise serializers.ValidationError('size field is required.')

        return value

    def create(self, validated_data):
        return Size.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.size_code = validated_data.get('size_code')
        instance.size = validated_data.get('size')

        return instance


class ColorSeriailizer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    color_name = serializers.CharField()
    color = serializers.CharField()

    def validate_color_name(self, value):
        if not value:
            raise serializers.ValidationError('color_name field is required.')

        return value

    def validate_color(self, value):
        if not value:
            raise serializers.ValidationError('color field is required.')

        return value

    def create(self, validated_data):
        return Color.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.color_name = validated_data('color_name')
        instance.color = validated_data('color')

        return instance


class DiscountSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    precent = serializers.CharField()

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('title field is required.')

        return value

    def validate_precent(self, value):
        if not value:
            raise serializers.ValidationError('Precent field is required.')

        return value

    def create(self, validated_data):
        return Discount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.precent = validated_data.get('precent')

        return instance


class ProductVariantSeriailzier(serializers.ModelSerializer):
    reference_id = serializers.CharField(read_only=True)

    class Meta:
        models = ProductVariant
        fields = ['reference_id', 'product', 'price',
                  'color', 'size', 'stock']


class ProductImageSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    image = serializers.ImageField()

    def create(self, validated_data):
        # # validated_data.pop('variant')
        # return ProductImage(**validated_data)
        pass

    def update(self, instance, validated_data):
        pass


class ProductSeriailzier(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    product_name = serializers.CharField()
    product_code = serializers.CharField()
    description = serializers.CharField()
    category = CategorySerializer()
    is_featured = serializers.BooleanField()
    is_recommend = serializers.BooleanField()
    thumbnail = serializers.ImageField()
    rating = serializers.IntegerField()
    slug = serializers.SlugField()
    discount = DiscountSerializer()
    variants = ProductVariantSeriailzier(many=True)
    images = ProductImageSerializer(many=True)

    def create(self, validated_data):
        with transaction.atomic():
            # creating transaction savepoint id
            sid = transaction.savepoint()

            try:
                variants = validated_data.pop('variants')
                images = validated_data.pop('images')

                product = Product.objects.create(**validated_data)

                for varinat in variants:
                    ProductVariant.objects.create(product=product, **varinat)

                for image in images:
                    ProductImage.objects.create(product=product, **image)

                transaction.savepoint_commit(sid)
                return product

            except Exception as exe:
                transaction.savepoint_rollback(sid)
                raise exe
 
    def update(self, instance, validated_data):
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                instance.product_name = validated_data.get('product_name')
                instance.product_code = validated_data.get('product_code')
                instance.description = validated_data.get('description')
                instance.is_featured = validated_data.get('is_featured')
                instance.is_recommend = validated_data.get('is_recommend')
                instance.thumbnail = validated_data.get('thumbnail')
                instance.rating = validated_data.get('rating')
                instance.slug = validated_data.get('slug')

                instance.discount = Discount.objects.get(
                    reference_id=validated_data.get('discount'))
                instance.category = Category.objects.get(
                    reference_id=validated_data.get('category'))

                variants = validated_data.pop('variants')
                images = validated_data.pop('images')

                for variant in variants:
                    variant_instance = ProductVariant.objects.get(
                        reference_id=variant.reference_id)

                    if variant_instance:
                        variant_instance.product = instance
                        variant_instance.price = variant.get('price')
                        variant_instance.size = variant.get('size')
                        variant_instance.stock = variant.get('stock')
                        variant_instance.save()

                    for image in images:
                        image_instance = ProductImage.objects.get(
                            reference_id=image.reference_id)

                        if image_instance:
                            image_instance.variant = variant
                            image_instance.image = image
                            image_instance.save()
                transaction.savepoint_commit(sid)
                return instance

            except Exception as exe:
                transaction.savepoint_rollback(sid)
                raise exe


class TagsSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    tag_name = serializers.CharField()
    # product = ProductSeriailzier(many=True)


    def create(self, validated_data):
        return Tags.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.tag_name = validated_data.get('tag_name')
        instance.save()

        return instance
