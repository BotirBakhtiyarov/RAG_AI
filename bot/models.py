# bot/models.py
from django.db import models

class KnowledgeBaseFile(models.Model):
    """Model to store uploaded files for the knowledge base."""
    file = models.FileField(upload_to='data/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded at {self.uploaded_at}"
