from datetime import datetime
from typing import Dict, Optional, Union, Any, cast
from uuid import uuid4

from .types import (
    AskOptions,
    JsonRPCRequest,
    Message,
    MessagePart,
    RequestId,
    SessionId,
    TaskId,
    TaskParams,
    TaskResponse,
    TaskStatusUpdateEvent,
    Task,
)

# Base URLs for different environments
BASE_URLS = {
    'LIVE': 'https://agent.payman.ai/api',
    'TEST': 'https://agent.payman.dev/api',
    'INTERNAL': 'https://payman.ngrok.dev/api',
}

# API Endpoints
API_ENDPOINTS = {
    'OAUTH_TOKEN': '/oauth2/token',
    'TASKS_SEND': '/a2a/tasks/send',
    'TASKS_SEND_SUBSCRIBE': '/a2a/tasks/sendSubscribe',
}

def generate_task_id() -> TaskId:
    """Generate a new task ID."""
    return f'tsk-{uuid4()}'

def generate_session_id() -> SessionId:
    """Generate a new session ID."""
    return f'ses-{uuid4()}'

def generate_request_id() -> RequestId:
    """Generate a new request ID."""
    return f'req-{uuid4()}'

def create_message(text: str, options: Optional[AskOptions] = None) -> Message:
    """Create a new message with the given text and options."""
    metadata: Optional[Dict[str, Any]] = None
    if options and options.get('message_metadata'):
        metadata = options['message_metadata']

    part_metadata: Optional[Dict[str, Any]] = None
    if options and options.get('part_metadata'):
        part_metadata = options['part_metadata']

    return {
        'role': 'user',
        'parts': [
            {
                'type': 'text',
                'text': text,
                'metadata': part_metadata,
            }
        ],
        'metadata': metadata,
    }

def create_task_request(
    message: Message,
    session_id: SessionId,
    options: Optional[AskOptions] = None,
) -> JsonRPCRequest[TaskParams]:
    """Create a new task request with the given message and session ID."""
    metadata: Dict[str, Any] = {
        'timestamp': datetime.utcnow().isoformat(),
    }
    if options and options.get('metadata'):
        metadata.update(options['metadata'] or {})

    return {
        'jsonrpc': '2.0',
        'id': generate_request_id(),
        'method': 'tasks.send',
        'params': {
            'id': generate_task_id(),
            'message': message,
            'session_id': session_id,
            'metadata': metadata,
        },
    }

def create_task_response_from_status_event(
    status_event: TaskStatusUpdateEvent,
) -> TaskResponse:
    """Create a TaskResponse from a TaskStatusUpdateEvent."""
    task: Task = {
        'id': status_event['id'],
        'session_id': None,
        'status': status_event['status'],
        'artifacts': [],
        'metadata': status_event['metadata'],
    }
    return {
        'jsonrpc': '2.0',
        'id': f'req-{status_event["id"][4:]}',
        'result': task,
        'error': None,
    } 