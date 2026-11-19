import os
import re
import uuid
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import ChatSession, Document, DocumentChunk, ChatMessage
from .serializers import ChatSessionSerializer, DocumentSerializer, ChatMessageSerializer
from .document_parser import parse_document_file, chunk_passages
from .rag_engine import GeminiChatService, REFUSAL_NO_DOC

PRELOADED_DOCX_PATH = os.path.join(settings.BASE_DIR, 'data', 'SKASC_Policy_Manual_2026_2027.docx')

def index_document_file(document, file_path):
    try:
        raw_text, passages = parse_document_file(file_path, document.file_type)
        if not raw_text.strip():
            document.status = 'failed'
            document.error_message = "No selectable text could be extracted from this document."
            document.save()
            return False

        document.raw_text = raw_text
        document.status = 'processing'
        document.save()

        # Delete any existing chunks
        document.chunks.all().delete()

        chunks_data = chunk_passages(
            passages,
            chunk_size=getattr(settings, 'DEFAULT_CHUNK_SIZE', 500),
            overlap=getattr(settings, 'DEFAULT_CHUNK_OVERLAP', 100)
        )

        chunk_objects = []
        for c in chunks_data:
            chunk_objects.append(DocumentChunk(
                document=document,
                chunk_index=c['chunk_index'],
                section_title=c['section_title'],
                page_number=c['page_number'],
                content=c['content'],
                token_count=c['token_count']
            ))

        DocumentChunk.objects.bulk_create(chunk_objects)
        document.status = 'ready'
        document.error_message = None
        document.save()
        return True

    except Exception as e:
        document.status = 'failed'
        document.error_message = str(e)
        document.save()
        return False


class SessionView(APIView):
    def post(self, request):
        """FR-24: Start a session; automatically attaches SKASC policy doc if requested"""
        session = ChatSession.objects.create(title="SKASC Policy Inquiry")
        
        # Preload the college policy Word document for RAG immediately
        preload = request.data.get('preload_skasc', True)
        if preload and os.path.exists(PRELOADED_DOCX_PATH):
            doc = Document.objects.create(
                session=session,
                filename="SKASC_Policy_Manual_2026_2027.docx",
                file_type="docx",
                file_size=os.path.getsize(PRELOADED_DOCX_PATH),
                status='processing'
            )
            index_document_file(doc, PRELOADED_DOCX_PATH)

        return Response({
            "session_id": session.id,
            "title": session.title,
            "created_at": session.created_at,
            "active_document": DocumentSerializer(session.documents.filter(status='ready').first()).data if session.documents.filter(status='ready').exists() else None
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        """List past sessions for chat history navigation"""
        sessions = ChatSession.objects.all()[:30]
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class SessionDetailView(APIView):
    def get(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id)
            messages = session.messages.all()
            doc = session.documents.filter(status='ready').first()
            return Response({
                "session_id": session.id,
                "title": session.title,
                "active_document": DocumentSerializer(doc).data if doc else None,
                "messages": ChatMessageSerializer(messages, many=True).data
            })
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, session_id):
        """FR-12, FR-24: Delete session and clear data"""
        try:
            session = ChatSession.objects.get(id=session_id)
            session.delete()
            return Response({"status": "Session deleted successfully"})
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)


class PreloadSKASCView(APIView):
    def post(self, request):
        """Feed model college policy word document for RAG"""
        session_id = request.data.get('session_id')
        if not session_id:
            session = ChatSession.objects.create(title="SKASC Policy Inquiry")
        else:
            session = ChatSession.objects.filter(id=session_id).first()
            if not session:
                session = ChatSession.objects.create(id=session_id, title="SKASC Policy Inquiry")

        if not os.path.exists(PRELOADED_DOCX_PATH):
            return Response({"error": "College Policy Word Document not found on server"}, status=status.HTTP_404_NOT_FOUND)

        # Deactivate old documents for this session (FR-6)
        session.documents.all().delete()

        doc = Document.objects.create(
            session=session,
            filename="SKASC_Policy_Manual_2026_2027.docx",
            file_type="docx",
            file_size=os.path.getsize(PRELOADED_DOCX_PATH),
            status='processing'
        )
        success = index_document_file(doc, PRELOADED_DOCX_PATH)

        return Response({
            "message": "SKASC Policy Manual Word document loaded and indexed for RAG",
            "session_id": session.id,
            "document": DocumentSerializer(doc).data,
            "success": success
        })


class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """FR-2, FR-3, FR-4, FR-6: Upload and process document"""
        uploaded_file = request.FILES.get('file')
        session_id = request.data.get('session_id')

        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # File size check (FR-4: Reject files over size limit)
        max_bytes = getattr(settings, 'DEFAULT_FILE_LIMIT_MB', 20) * 1024 * 1024
        if uploaded_file.size > max_bytes:
            return Response({
                "error": f"File size exceeds the {settings.DEFAULT_FILE_LIMIT_MB} MB limit."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Extension check (FR-3: Accept PDF, DOCX, TXT)
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext not in ['pdf', 'docx', 'txt']:
            return Response({
                "error": f"Unsupported file type .{ext}. Only PDF, DOCX, and TXT files are supported."
            }, status=status.HTTP_400_BAD_REQUEST)

        session = None
        if session_id:
            session = ChatSession.objects.filter(id=session_id).first()
        if not session:
            session = ChatSession.objects.create(title=f"Chat: {uploaded_file.name[:25]}")

        # FR-6: Replacing document deletes old document, its index and chat context
        session.documents.all().delete()
        session.messages.all().delete()

        doc = Document.objects.create(
            session=session,
            file=uploaded_file,
            filename=uploaded_file.name,
            file_type=ext,
            file_size=uploaded_file.size,
            status='processing'
        )

        # Index document immediately
        file_path = doc.file.path
        success = index_document_file(doc, file_path)

        return Response({
            "document_id": doc.id,
            "session_id": session.id,
            "status": doc.status,
            "error_message": doc.error_message,
            "document": DocumentSerializer(doc).data
        }, status=status.HTTP_201_CREATED)


class DocumentDetailView(APIView):
    def get(self, request, doc_id):
        """FR-5: Check processing status"""
        try:
            doc = Document.objects.get(id=doc_id)
            return Response(DocumentSerializer(doc).data)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, doc_id):
        """FR-12: Delete document and its index"""
        try:
            doc = Document.objects.get(id=doc_id)
            doc.delete()
            return Response({"status": "Document and its index deleted successfully."})
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)


class ChatView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        """FR-13, FR-14, FR-20, FR-21: Handle user question"""
        session_id = request.data.get('session_id')
        question = request.data.get('question', '').strip()
        policy_filter = request.data.get('policy_filter', 'All Policies')

        if not question:
            return Response({"error": "Question cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        session = None
        if session_id:
            session = ChatSession.objects.filter(id=session_id).first()
        if not session:
            session = ChatSession.objects.create(title=question[:35])

        # If title is default, update with first question
        if session.title in ["New Policy Inquiry", "New Chat", "SKASC Policy Inquiry"] and len(question) > 2:
            session.title = question[:35] + ("..." if len(question) > 35 else "")
            session.save()

        # Get active document for this session
        document = session.documents.filter(status='ready').first()
        if not document:
            # Fall back to any active ready document or preload SKASC
            document = Document.objects.filter(status='ready').first()
            if not document and os.path.exists(PRELOADED_DOCX_PATH):
                document = Document.objects.create(
                    session=session,
                    filename="SKASC_Policy_Manual_2026_2027.docx",
                    file_type="docx",
                    file_size=os.path.getsize(PRELOADED_DOCX_PATH),
                    status='processing'
                )
                index_document_file(document, PRELOADED_DOCX_PATH)

        if not document or document.status != 'ready':
            # FR-7, TC-15: "Please upload a document first."
            user_msg = ChatMessage.objects.create(
                session=session,
                role='user',
                content=question
            )
            bot_msg = ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=REFUSAL_NO_DOC,
                reply_type='refusal'
            )
            return Response({
                "answer": REFUSAL_NO_DOC,
                "reply_type": "refusal",
                "policy_tags": [],
                "source_passages": [],
                "user_message_id": user_msg.id,
                "assistant_message_id": bot_msg.id,
                "session_id": session.id
            })

        # Save user message
        user_msg = ChatMessage.objects.create(
            session=session,
            role='user',
            content=question
        )

        # Call RAG engine
        result = GeminiChatService.ask(
            question=question,
            document=document,
            policy_filter=policy_filter,
            session_id=session.id
        )

        # Save assistant message
        bot_msg = ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=result['answer'],
            reply_type=result['reply_type'],
            policy_tags=result.get('policy_tags', []),
            source_passages=result.get('source_passages', [])
        )

        return Response({
            "answer": result['answer'],
            "reply_type": result['reply_type'],
            "policy_tags": result['policy_tags'],
            "source_passages": result['source_passages'],
            "user_message_id": user_msg.id,
            "assistant_message_id": bot_msg.id,
            "session_id": session.id,
            "timestamp": bot_msg.created_at
        })


class PolicyListView(APIView):
    def get(self, request):
        """Returns the list of policies / sections found in the current document"""
        session_id = request.query_params.get('session_id')
        document = None
        if session_id:
            session = ChatSession.objects.filter(id=session_id).first()
            if session:
                document = session.documents.filter(status='ready').first()
        if not document:
            document = Document.objects.filter(status='ready').first()

        policies = ["All Policies"]
        if document:
            sections = document.chunks.values_list('section_title', flat=True).distinct()
            cleaned_sections = []
            for s in sections:
                # Remove clause sub-tag e.g. " (Clause 1.1)"
                clean_name = re.sub(r'\s*\(Clause\s+[\d\.]+\)', '', s).strip()
                if clean_name and clean_name not in cleaned_sections and clean_name not in ['General', 'General / Introduction', 'Contents', 'Preface']:
                    cleaned_sections.append(clean_name)
            
            # Sort or prioritize known policy sections
            policies.extend(cleaned_sections)
        else:
            policies.extend([
                "1. About the College, Governance and Applicability",
                "2. Admission Policy",
                "3. Academic Policy",
                "4. Attendance Policy",
                "5. Examination and Evaluation Policy",
                "6. Fee Structure, Payment and Refund Policy",
                "7. Scholarship and Financial Assistance Policy",
                "8. Student Code of Conduct and Discipline Policy",
                "9. Anti-Ragging Policy",
                "10. Prevention of Sexual Harassment and Gender Equity Policy",
                "11. Grievance Redressal and Equal Opportunity Policy",
                "12. Library Policy",
                "13. Information Technology and Acceptable Use Policy",
                "14. Data Privacy and Records Management Policy",
                "15. Campus Safety, Security and Health Policy",
                "16. Hostel Policy",
                "17. Transport Policy",
                "18. Placement and Career Development Policy",
                "19. Research, Publication Ethics and Anti-Plagiarism Policy",
                "20. Faculty and Staff Service Policy",
                "21. Leave Policy for Staff",
                "22. Financial Management, Procurement and Audit Policy",
                "23. Infrastructure, Maintenance and Environmental Sustainability Policy",
                "24. Internal Quality Assurance, Accreditation and Compliance Policy",
                "25. Policy Review, Amendment and Interpretation"
            ])

        return Response({"policies": policies})


class SettingsView(APIView):
    def get(self, request):
        has_key = bool(getattr(settings, 'GEMINI_API_KEY', '') or os.environ.get('GEMINI_API_KEY', ''))
        return Response({
            "has_gemini_key": has_key,
            "gemini_model": getattr(settings, 'GEMINI_MODEL_NAME', 'gemini-1.5-flash'),
            "file_limit_mb": getattr(settings, 'DEFAULT_FILE_LIMIT_MB', 20),
            "chunk_size": getattr(settings, 'DEFAULT_CHUNK_SIZE', 500),
            "chunk_overlap": getattr(settings, 'DEFAULT_CHUNK_OVERLAP', 100)
        })

    def post(self, request):
        api_key = request.data.get('gemini_api_key')
        model_name = request.data.get('gemini_model')
        if api_key is not None:
            settings.GEMINI_API_KEY = api_key.strip()
            os.environ['GEMINI_API_KEY'] = api_key.strip()
        if model_name:
            settings.GEMINI_MODEL_NAME = model_name.strip()
        return Response({
            "status": "Settings updated",
            "has_gemini_key": bool(settings.GEMINI_API_KEY),
            "gemini_model": settings.GEMINI_MODEL_NAME
        })
