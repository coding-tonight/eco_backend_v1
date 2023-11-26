from rest_framework import serializers

from item.models import Color ,Size


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
    pass