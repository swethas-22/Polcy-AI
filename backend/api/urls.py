from django.urls import path
from .views import (
    SessionView,
    SessionDetailView,
    DocumentUploadView,
    DocumentDetailView,
    PreloadSKASCView,
    ChatView,
    PolicyListView,
    SettingsView
)

urlpatterns = [
    path('sessions', SessionView.as_view(), name='sessions'),
    path('sessions/<str:session_id>', SessionDetailView.as_view(), name='session_detail'),
    path('documents', DocumentUploadView.as_view(), name='document_upload'),
    path('documents/<str:doc_id>', DocumentDetailView.as_view(), name='document_detail'),
    path('documents/preload_skasc', PreloadSKASCView.as_view(), name='preload_skasc'),
    path('chat', ChatView.as_view(), name='chat'),
    path('policies', PolicyListView.as_view(), name='policies'),
    path('settings', SettingsView.as_view(), name='settings'),
]
