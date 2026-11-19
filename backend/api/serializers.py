from rest_framework import serializers
from .models import ChatSession, Document, DocumentChunk, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'role', 'content', 'reply_type', 'policy_tags', 'source_passages', 'created_at']


class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ['id', 'chunk_index', 'section_title', 'page_number', 'content', 'token_count']


class DocumentSerializer(serializers.ModelSerializer):
    chunks_count = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'session', 'filename', 'file_type', 'file_size', 'status', 'error_message', 'uploaded_at', 'chunks_count']

    def get_chunks_count(self, obj):
        return obj.chunks.count()


class ChatSessionSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'created_at', 'updated_at', 'documents', 'messages_count']

    def get_messages_count(self, obj):
        return obj.messages.count()
