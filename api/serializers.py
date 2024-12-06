# chatbot/serializers.py
from rest_framework import serializers

class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
