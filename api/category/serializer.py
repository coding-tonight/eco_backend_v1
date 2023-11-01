from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    category_name = serializers.CharField()
    icon_url = serializers.ImageField(required=False)

    # def validate_category_name(self, data):
    #     return 

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance ,validated_data):
        instance.category_name = validated_data['category_name']
        instance.icon_url = validated_data['icon_url']
        instance.save()

        return instance