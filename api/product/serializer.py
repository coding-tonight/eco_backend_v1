from rest_framework import serializers
from product.models import Size, Color, Discount


from category.serializer import CategorySerializer
from category.models import Category



class  SizeSerializer(serializers.Serializer):
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


    def update(self, instance , validated_data):
        instance.size_code = validated_data.get('size_code')
        instance.size =validated_data.get('size')

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
    
    def update(self, instance , validated_data):
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
        instance.title4 = validated_data.get('title')
        instance.precent = validated_data.get('precent')

        return instance



class ProductVariantSeriailzier(serializers.ModelSerializer):
    reference_id = serializers.CharField(read_only=True)


class ProductSeriailzier(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    product_name = serializers.CharField()
    product_code = serializers.CharField()
    description = serializers.CharField()
    category = CategorySerializer(many=True)
    is_featured = serializers.BooleanField()
    is_recommend = serializers.BooleanField()
    thumbnail = serializers.ImageField()
    discount = DiscountSerializer(many=True)
    rating = serializers.IntegerField()
    slug = serializers.SlugField()


    def create(self, validated_data):
        pass




