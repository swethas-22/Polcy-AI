import uuid
from django.db import models

class ChatSession(models.Model):
    id = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="New Policy Inquiry")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.id[:8]})"


class Document(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]

    id = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=16)  # pdf, docx, txt
    file_size = models.BigIntegerField(default=0)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='processing')
    error_message = models.TextField(blank=True, null=True)
    raw_text = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.filename} [{self.status}]"


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField()
    section_title = models.CharField(max_length=255, default='General')
    page_number = models.IntegerField(default=1)
    content = models.TextField()
    token_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['chunk_index']

    def __str__(self):
        return f"{self.document.filename} - [{self.section_title} P.{self.page_number}] #{self.chunk_index}"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    REPLY_TYPE_CHOICES = [
        ('answer', 'Answer'),
        ('refusal', 'Refusal'),
        ('error', 'Error'),
    ]

    id = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    content = models.TextField()
    reply_type = models.CharField(max_length=16, choices=REPLY_TYPE_CHOICES, default='answer')
    policy_tags = models.JSONField(default=list, blank=True)
    source_passages = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.role}] {self.content[:40]}..."
