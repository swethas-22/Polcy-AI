import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polcy_backend.settings')
django.setup()

from rest_framework.test import APIClient
from api.models import ChatSession, Document

def test_rest_api():
    client = APIClient()
    print("=== Testing Django REST API Endpoints ===")

    # 1. Create Session
    res = client.post('/api/sessions', {'preload_skasc': True}, format='json')
    print(f"[1] POST /api/sessions -> Status: {res.status_code}")
    assert res.status_code == 201
    data = res.json()
    session_id = data['session_id']
    print(f"    Session ID: {session_id}, Active doc: {data.get('active_document', {}).get('filename')}")

    # 2. Query Policies
    res_pol = client.get('/api/policies')
    print(f"[2] GET /api/policies -> Status: {res_pol.status_code}")
    assert res_pol.status_code == 200
    policies = res_pol.json()['policies']
    print(f"    Found {len(policies)} policies (e.g. {policies[1:4]})")
    assert len(policies) >= 20

    # 3. Query Chat - Minimum attendance percentage
    res_chat1 = client.post('/api/chat', {
        'session_id': session_id,
        'question': 'What is the minimum attendance percentage?',
        'policy_filter': 'All Policies'
    }, format='json')
    print(f"[3] POST /api/chat (Attendance) -> Status: {res_chat1.status_code}")
    assert res_chat1.status_code == 200
    chat_data1 = res_chat1.json()
    print(f"    Reply Type: {chat_data1['reply_type']}")
    print(f"    Policy Tags: {chat_data1['policy_tags']}")
    print(f"    Answer Preview: {chat_data1['answer'][:120]}...")
    assert "75%" in chat_data1['answer']
    assert chat_data1['reply_type'] == 'answer'

    # 4. Query Chat - Unrelated general knowledge question
    res_chat2 = client.post('/api/chat', {
        'session_id': session_id,
        'question': 'What is the capital of France?',
        'policy_filter': 'All Policies'
    }, format='json')
    print(f"[4] POST /api/chat (Unrelated) -> Status: {res_chat2.status_code}")
    chat_data2 = res_chat2.json()
    print(f"    Reply Type: {chat_data2['reply_type']}")
    print(f"    Answer: {chat_data2['answer']}")
    assert chat_data2['reply_type'] == 'refusal'
    assert chat_data2['answer'] == "I can only answer questions about the uploaded document."

    # 5. Query Chat - Absent policy question
    res_chat3 = client.post('/api/chat', {
        'session_id': session_id,
        'question': 'Can I ride a dolphin in the college pond?',
        'policy_filter': 'All Policies'
    }, format='json')
    print(f"[5] POST /api/chat (Not Found) -> Status: {res_chat3.status_code}")
    chat_data3 = res_chat3.json()
    print(f"    Reply Type: {chat_data3['reply_type']}")
    print(f"    Answer: {chat_data3['answer']}")
    assert chat_data3['reply_type'] == 'refusal'
    assert chat_data3['answer'] == "I could not find this in the uploaded document."

    # 6. Verify Session Details & History
    res_sess = client.get(f'/api/sessions/{session_id}')
    print(f"[6] GET /api/sessions/{session_id} -> Status: {res_sess.status_code}")
    sess_data = res_sess.json()
    print(f"    Total messages recorded: {len(sess_data['messages'])}")
    assert len(sess_data['messages']) >= 6

    # 7. Check Settings endpoint
    res_set = client.get('/api/settings')
    print(f"[7] GET /api/settings -> Status: {res_set.status_code}")
    assert res_set.status_code == 200

    print("\n=== ALL REST API ENDPOINTS VALIDATED SUCCESSFULLY ===")

if __name__ == "__main__":
    test_rest_api()
