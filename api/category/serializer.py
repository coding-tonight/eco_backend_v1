from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    category_name = serializers.CharField()
    icon_url = serializers.ImageField(required=False)
    # slug = Category.get_absolute_url()

    # def validate_category_name(self, data):
    #     return 

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance ,validated_data):
        instance.category_name = validated_data.get('category_name')
        instance.icon_url = validated_data.get('icon_url')
        instance.save()

        return instance