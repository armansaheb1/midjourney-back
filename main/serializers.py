from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ImagineOrder, Image, Transaction, FaceSwaped, Plan, Bonus, GPTMessages, GPTChatRoom, Parameter, Permissions,AddDetail , Post, Link

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = (
            'gpt',
        )

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        depth= 1
        fields = (
            'id',
            'username',
            'email',
            'is_superuser',
            'permissionss'
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
            "get_age",
            "code"
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
        

class GPTMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPTMessages
        fields = (
            "id",
            "room",
            "role",
            "message",
            "date",
        )


class GPTChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPTChatRoom
        depth = 1
        fields = (
            "get_age",
            "first_message",
            "id"
        )

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddDetail
        depth = 1
        fields = (
            "title",
            "prompt",
            "image",
            "get_image"
        )

class ParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        depth = 1
        fields = (
            "title",
            "prompt",
            "minimum",
            "maximum",
            "default"
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        depth = 1
        fields = (
            "id",
            "content",
            "get_file"
        )


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        depth = 1
        fields = (
            "title",
            "link",
        )