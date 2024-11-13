from rest_framework import serializers
from django.contrib.auth.models import User
from .models import GPTMessages, GPTChatRoom

class GPTMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPTMessages
        fields = (
            "id",
            "room",
            "role",
            "message",
            "date",
            "like"
        )


class GPTChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPTChatRoom
        depth = 1
        fields = (
            "get_age",
            "first_message",
            "organization",
            "id"
        )