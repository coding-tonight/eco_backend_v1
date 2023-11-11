from rest_framework import serializers

from metadata.models import MetaData


class MetaDataSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    app_name = serializers.CharField(required=True, error_messages={
                                     'required': 'app_name is required'})
    contact_number = serializers.CharField(required=True, error_messages={
                                           'required': 'contact number is required'})
    address = serializers.CharField(required=True, error_messages={
        'required': 'address is required'
    })
    logo = serializers.ImageField()

    def validate_app_name(self, value):
        if value is None:
            raise serializers.ValidationError('App name can be null.')

        return value

    def validate_logo(self, value):
        pass

    def create(self, validated_data):
        return MetaData.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.app_name = validated_data.get('app_name')
        instance.contact_number = validated_data.get('contact_number')
        instance.address = validated_data.get('address')
        instance.save()

        return instance
