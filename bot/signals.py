# chatbot/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import KnowledgeBaseFile
from .chatbot_logic import update_knowledge_base, load_knowledge_base
import os


@receiver(post_save, sender=KnowledgeBaseFile)
def update_knowledge_base_on_upload(sender, instance, created, **kwargs):
    if created:  # Only trigger when a new file is uploaded
        file_path = instance.file.path
        print(f"New file uploaded: {file_path}")

        # Update the knowledge base with the uploaded file
        vector_store = load_knowledge_base("media/data")  # Reload knowledge base
        update_knowledge_base(vector_store, file_path)
