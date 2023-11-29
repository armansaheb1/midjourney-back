from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ImagineOrder, Image, Transaction, FaceSwaped, Plan, Bonus

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'is_superuser'
        )

class ImagineOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagineOrder
        fields = (
            "id",
            "user", 
            "username",
            "text",
            "date",
            "code",
            "percent",
            "done",
            "result",
            "image",
            "get_age",
            "get_variations",
            "act",
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


class FaceSwapedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceSwaped
        fields = (
            "user", 
            "username",
            "fsid", 
            "image", 
            "get_age"
        )

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "id", 
            "price", 
            "coin", 
        )


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = (
            "id",
            "user",
            "username", 
            "code", 
            "amount", 
        )