from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ImagineOrder, Image, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )

class ImagineOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagineOrder
        fields = (
            "id",
            "user", 
            "text",
            "date",
            "code",
            "percent",
            "done",
            "result",
            "image",
            "get_age",
            "get_variations",
            "bid",
            "buttons",
            "type"
        )

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Image
        fields = (
            "image", 
            "get_image"

        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "user", 
            "amount",
            "username",
            "get_age"

        )