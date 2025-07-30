from enum import Enum
from typing import Any, Callable, Dict, Generic, List, Optional, TypedDict, Union, Literal, TypeVar
from uuid import uuid4

# Type variable for generic types
T = TypeVar('T')

# Environment type
Environment = Literal['TEST', 'LIVE', 'INTERNAL']

# ID Types
TaskId = str  # Format: tsk-{uuid}
SessionId = str  # Format: ses-{uuid}
RequestId = str  # Format: req-{uuid}

class PaymanConfig(TypedDict):
    client_id: str
    client_secret: Optional[str]
    environment: Optional[Environment]

class OAuthResponse(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    scope: str

class MessagePart(TypedDict):
    type: Literal['text']
    text: str
    metadata: Optional[Dict[str, Any]]

class Message(TypedDict):
    role: Literal['user', 'assistant']
    parts: List[MessagePart]
    metadata: Optional[Dict[str, Any]]

class TaskState(str, Enum):
    SUBMITTED = 'submitted'
    WORKING = 'working'
    INPUT_REQUIRED = 'input-required'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    FAILED = 'failed'
    UNKNOWN = 'unknown'

class TaskStatus(TypedDict):
    state: TaskState
    message: Optional[Message]
    timestamp: str

class FormattedArtifact(TypedDict):
    name: str
    description: Optional[str]
    content: str
    type: str
    timestamp: str
    metadata: Optional[Dict[str, Any]]

class Artifact(TypedDict):
    name: Optional[str]
    description: Optional[str]
    parts: List[MessagePart]
    index: Optional[int]
    append: Optional[bool]
    metadata: Optional[Dict[str, Any]]
    last_chunk: Optional[bool]

class Task(TypedDict):
    id: TaskId
    session_id: Optional[SessionId]
    status: TaskStatus
    artifacts: List[Artifact]
    metadata: Dict[str, Any]

class AgentCapabilities(TypedDict):
    streaming: bool
    push_notifications: bool
    state_transition_history: bool

class AgentProvider(TypedDict):
    organization: str
    url: str

class AgentAuthentication(TypedDict):
    schemes: List[str]
    credentials: Optional[str]

class AgentSkill(TypedDict):
    id: str
    name: str
    description: Optional[str]
    tags: Optional[List[str]]
    examples: Optional[List[str]]
    input_modes: Optional[List[str]]
    output_modes: Optional[List[str]]

class AgentCard(TypedDict):
    name: str
    description: Optional[str]
    url: str
    provider: AgentProvider
    version: str
    documentation_url: Optional[str]
    capabilities: AgentCapabilities
    authentication: AgentAuthentication
    default_input_modes: List[str]
    default_output_modes: List[str]
    skills: List[AgentSkill]

# JSON-RPC Types
class JsonRPCRequest(TypedDict, Generic[T]):
    jsonrpc: Literal['2.0']
    id: RequestId
    method: str
    params: T

class TaskParams(TypedDict):
    id: TaskId
    message: Message
    session_id: SessionId
    metadata: Optional[Dict[str, Any]]

class TaskGetParams(TypedDict):
    id: TaskId

class TaskCancelParams(TypedDict):
    id: TaskId

class AskOptions(TypedDict, Generic[T]):
    new_session: Optional[bool]
    metadata: Optional[Dict[str, Any]]
    part_metadata: Optional[Dict[str, Any]]
    message_metadata: Optional[Dict[str, Any]]
    on_message: Optional[Callable[[Message], None]]

class TaskStatusUpdateEvent(TypedDict):
    id: TaskId
    status: TaskStatus
    is_final: bool
    metadata: Dict[str, Any]

class TaskArtifactUpdateEvent(TypedDict):
    id: TaskId
    artifact: Artifact

# Response Types
class A2AError(TypedDict):
    code: int
    message: str
    data: Optional[Any]

class JsonRPCResponse(TypedDict, Generic[T]):
    jsonrpc: Literal['2.0']
    id: RequestId
    result: Optional[T]
    error: Optional[A2AError]

class FormattedTaskResponse(TypedDict):
    task_id: TaskId
    request_id: RequestId
    session_id: Optional[SessionId]
    status: TaskState
    status_message: Optional[str]
    timestamp: str
    artifacts: List[FormattedArtifact]
    metadata: Dict[str, Any]
    error: Optional[A2AError]

# Type aliases
TaskResponse = JsonRPCResponse[Task]
AgentCardResponse = AgentCard
TaskStatusUpdateResponse = JsonRPCResponse[TaskStatusUpdateEvent]
TaskArtifactUpdateResponse = JsonRPCResponse[TaskArtifactUpdateEvent] 