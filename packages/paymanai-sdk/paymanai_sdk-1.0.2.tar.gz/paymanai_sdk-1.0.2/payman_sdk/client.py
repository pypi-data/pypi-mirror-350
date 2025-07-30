import base64
from datetime import datetime
from typing import Dict, Optional, Union, Callable, Any, cast, List
import requests

from .types import (
    AskOptions,
    Environment,
    FormattedTaskResponse,
    OAuthResponse,
    PaymanConfig,
    SessionId,
    TaskResponse,
    TaskState,
    A2AError,
    FormattedArtifact,
)
from .utils import (
    API_ENDPOINTS,
    BASE_URLS,
    create_message,
    create_task_request,
    generate_session_id,
)

class PaymanClient:
    """
    Client for interacting with the Payman AI Platform

    Example:
        ```python
        # Initialize with client credentials
        payman = PaymanClient.with_credentials({
            'client_id': 'your-client-id',
            'client_secret': 'your-client-secret',
            'environment': 'TEST'  # optional, defaults to 'LIVE'
        })

        # Initialize with authorization code
        payman = PaymanClient.with_auth_code({
            'client_id': 'your-client-id',
            'client_secret': 'your-client-secret',
            'environment': 'TEST'
        }, 'your-auth-code')

        # Initialize with pre-existing access token
        payman = PaymanClient.with_token(
            'your-client-id',
            {
                'access_token': 'your-access-token',
                'expires_in': 3600  # token expiry in seconds
            },
            'TEST'
        )

        # Get a formatted response (recommended for most use cases)
        formatted_response = await payman.ask("What's the weather?")

        # Get a raw response
        raw_response = await payman.ask("What's the weather?", raw=True)

        # Streaming request with formatted responses
        await payman.ask("What's the weather?", {
            'on_message': lambda response: print(f"Formatted response: {response}")
        })

        # Start a new session with metadata
        response = await payman.ask("Hello!", {
            'new_session': True,
            'metadata': {'source': 'web-app'}
        })
        ```
    """

    def __init__(
        self,
        config: PaymanConfig,
        auth_code: Optional[str] = None,
        token_info: Optional[Dict[str, Any]] = None,
    ):
        """
        Creates a new PaymanClient instance with full configuration

        Args:
            config: Configuration for the client
            auth_code: Optional authorization code obtained via OAuth
            token_info: Optional object containing pre-existing access token information
        """
        self.config = config
        self.session_id = generate_session_id()
        env = config.get('environment', 'LIVE')
        self.base_url = BASE_URLS[cast(Environment, env)]
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

        if token_info:
            self.access_token = token_info['access_token']
            self.token_expiry = datetime.now().timestamp() + token_info['expires_in']
            self.is_token_refreshable = False
        else:
            self.is_token_refreshable = True
            self._initialize_access_token(auth_code)

    @classmethod
    def with_credentials(cls, config: PaymanConfig) -> 'PaymanClient':
        """Creates a new PaymanClient instance with client credentials."""
        return cls(config)

    @classmethod
    def with_auth_code(cls, config: PaymanConfig, auth_code: str) -> 'PaymanClient':
        """Creates a new PaymanClient instance with an authorization code."""
        return cls(config, auth_code=auth_code)

    @classmethod
    def with_token(
        cls,
        client_id: str,
        token_info: Dict[str, Any],
        environment: Environment = 'LIVE',
    ) -> 'PaymanClient':
        """Creates a new PaymanClient instance with just client ID and access token."""
        config: PaymanConfig = {
            'client_id': client_id,
            'environment': environment,
            'client_secret': None
        }
        return cls(config, token_info=token_info)

    def _initialize_access_token(self, auth_code: Optional[str] = None) -> None:
        """
        Initializes or refreshes the OAuth access token

        Args:
            auth_code: Optional authorization code. If provided, uses authorization_code grant type,
                      otherwise uses client_credentials
        """
        try:
            params = {
                'grant_type': 'authorization_code' if auth_code else 'client_credentials',
            }
            if auth_code:
                params['code'] = auth_code

            auth = base64.b64encode(
                f"{self.config['client_id']}:{self.config['client_secret']}".encode()
            ).decode()

            response = self.session.post(
                f"{self.base_url}{API_ENDPOINTS['OAUTH_TOKEN']}",
                params=params,
                headers={'Authorization': f'Basic {auth}'},
            )
            response.raise_for_status()
            data: OAuthResponse = response.json()

            self.access_token = data['access_token']
            self.token_expiry = datetime.now().timestamp() + data['expires_in']
        except Exception as e:
            print(f'Failed to initialize access token: {e}')
            if hasattr(e, 'response'):
                print(f'Response data: {e.response.json()}')
                print(f'Response status: {e.response.status_code}')
            raise

    def _ensure_valid_access_token(self) -> str:
        """
        Ensures the access token is valid and refreshes it if necessary

        Returns:
            A valid access token

        Raises:
            Error: If token cannot be obtained or if non-refreshable token has expired
        """
        now = datetime.now().timestamp()
        if not hasattr(self, 'access_token') or not hasattr(self, 'token_expiry') or now >= self.token_expiry - 60:
            if not self.is_token_refreshable:
                raise Exception('Access token has expired and cannot be refreshed')
            self._initialize_access_token()

        if not hasattr(self, 'access_token'):
            raise Exception('Failed to obtain access token')

        return cast(str, self.access_token)

    def ask(
        self,
        text: str,
        options: Optional[AskOptions] = None,
        raw: bool = False,
    ) -> Union[FormattedTaskResponse, TaskResponse]:
        """
        Ask a question or send a message to the Payman AI Agent

        Args:
            text: The message or question to send to the agent
            options: Optional parameters for the request
            raw: Whether to return raw responses instead of formatted ones

        Returns:
            The task response (formatted or raw)
        """
        token = self._ensure_valid_access_token()

        if options and options.get('new_session'):
            self.session_id = generate_session_id()

        message = create_message(text, options)
        request = create_task_request(message, self.session_id, options)

        response = self.session.post(
            f"{self.base_url}{API_ENDPOINTS['TASKS_SEND']}",
            json=request,
            headers={'x-payman-access-token': token},
        )
        response.raise_for_status()
        data: TaskResponse = response.json()

        if data.get('error'):
            raise Exception(f"Failed to get response from agent: {data['error']}")

        if not data.get('result'):
            raise Exception('No response received from agent')

        if raw:
            return data

        return self._format_response(data)

    def _format_response(self, response: TaskResponse) -> FormattedTaskResponse:
        """Formats a TaskResponse into a more developer-friendly structure."""
        if response.get('error'):
            return {
                'task_id': response['id'],
                'request_id': response['id'],
                'session_id': None,
                'status': TaskState.FAILED,
                'status_message': None,
                'timestamp': datetime.utcnow().isoformat(),
                'artifacts': [],
                'metadata': {},
                'error': response['error'],
            }

        if not response.get('result'):
            raise Exception('Response has no result and no error')

        result = response['result']
        if not result:
            raise Exception('Response result is None')

        formatted_artifacts: List[FormattedArtifact] = []
        for artifact in result.get('artifacts', []):
            content = '\n'.join(part['text'] for part in artifact.get('parts', []))
            formatted_artifacts.append({
                'name': artifact.get('name') or 'artifact',
                'description': artifact.get('description'),
                'content': content,
                'type': 'text',
                'timestamp': datetime.utcnow().isoformat(),
                'metadata': artifact.get('metadata', {}),
            })

        return {
            'task_id': result['id'],
            'request_id': response['id'],
            'session_id': result.get('session_id'),
            'status': result['status']['state'],
            'status_message': None,
            'timestamp': result['status']['timestamp'],
            'artifacts': formatted_artifacts,
            'metadata': result.get('metadata', {}),
            'error': None,
        }

    def get_access_token(self) -> Optional[Dict[str, Any]]:
        """Gets the current access token information."""
        if not hasattr(self, 'access_token'):
            return None

        return {
            'access_token': self.access_token,
            'expires_in': int(self.token_expiry - datetime.now().timestamp()),
        }

    def is_access_token_expired(self) -> bool:
        """Checks if the current access token has expired."""
        if not hasattr(self, 'token_expiry'):
            return True

        return bool(datetime.now().timestamp() >= self.token_expiry - 60) 