# chatbot/urls.py
from django.urls import path
from .views import ChatbotAPI

urlpatterns = [
    path('chat/', ChatbotAPI.as_view(), name='chatbot-api'),
]