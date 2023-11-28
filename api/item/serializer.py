from rest_framework import serializers
from rest_framework.reverse import reverse

from item.models import Color ,Size, Product


class ColorSerilaizer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    color_name = serializers.CharField()
    color_code = serializers.CharField()

    def validate_color_name(self, value):
        if not value:
            raise serializers.ValidationError('Color name can not be null.')
        
        return value
    
    def validdate_color_code(self, value):
        if not value:
            raise serializers.ValidationError('Color code can notbe null')
        
        return value

    def create(self, **validated_data): 
        return Color.objects.create(**validated_data)

    def update(self, instance , **validated_data):
        instance.color_name = validated_data.get('color_name')
        instance.color_code = validated_data.get('color_code')
        instance.save()

        return instance
    

class SizeSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    size = serializers.CharField()
    
    def validate_size(self ,value):
        if not value:
            raise serializers.ValidationError('value can not be null')
        
        return value

    def create(self, **validated_data):
        return Size.objects.create(**validated_data)

    def update(self, instance , **validated_data):
        instance.size = validated_data.get('size')
        instance.save()

        return instance



class ProductSerializer(serializers.HyperlinkedModelSerializer):
    reference_id = serializers.CharField(read_only=True)
    category = serializers.StringRelatedField(many=True)
    discount = serializers.StringRelatedField(many=True)

    class Meta:
        model =  Product
        fields = ['reference_id', 'product_name', 'category', 'slug', 
                  'discount', 'thumbnail', 'featured', 'recommeded']
        


class ProductVariant(serializers.HyperlinkedRelatedField):
    # defining  these as class attributes , so we don't need  to pass them as arguments
    view_name = 'product-detail'
    queryset = Product.objects.filter(is_delete=False)

    def get_url(self, obj, view_name, request, format):
        url_kwrags = {
            'product_slug': obj.product.slug,
            'reference_id': obj.reference_id
        }

        return reverse(view_name , url_kwrags=url_kwrags, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
          'product_slug': view_kwargs.get('product_slug'),
          'ref_id': view_kwargs.get('reference_id')

        }
        return super().get_queryset().get(**lookup_kwargs)
    


class Tags(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    # slug = serializers.SlugField()
    product = ProductSerializer(many=True)

    def create(self, **validated_data):
        return Tags.create(**validated_data)
    
    def update(self, instance, **validated_data):
        instance.title = validated_data.get('title')
        instance.save()

        return instance
        

