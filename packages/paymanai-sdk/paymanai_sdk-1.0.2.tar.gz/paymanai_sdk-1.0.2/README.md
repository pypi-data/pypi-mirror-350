# Payman SDK Python

This SDK provides a simple way to interact with the Payman AI Platform's API using client credentials authentication. The SDK automatically handles token management, including fetching and refreshing access tokens.

## Installation

### Prerequisites
- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Setup
```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/payman-ai/payman-sdk-python.git
cd payman-sdk-python

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## Environment Setup

Before running the SDK or tests, you need to set up your environment variables. Create a `.env` file in the root directory with the following variables:

```bash
PAYMAN_CLIENT_ID=your-client-id
PAYMAN_CLIENT_SECRET=your-client-secret
```

These credentials are required for both running the SDK and executing tests.

## Development

### Project Structure
```
payman-sdk-python/
├── payman_sdk/          # Main package directory
│   ├── __init__.py     # Package initialization
│   ├── client.py       # Main client implementation
│   ├── types.py        # Type definitions
│   └── utils.py        # Utility functions
├── tests/              # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_client.py
│   ├── test_types.py
│   └── test_utils.py
├── pyproject.toml      # Poetry configuration
├── poetry.lock         # Locked dependencies
├── pytest.ini         # Pytest configuration
├── CHANGELOG.md       # Version history
└── README.md          # This file
```

### Development Workflow

1. **Setup Development Environment**
```bash
# Install all dependencies including development tools
poetry install

# Activate virtual environment
poetry shell
```

2. **Running Tests**
```bash
# Run all tests with coverage
poetry run pytest

# Run specific test file
poetry run pytest tests/test_client.py -v

# Run tests with coverage report
poetry run pytest --cov=payman_sdk --cov-report=html
```

3. **Code Quality**
```bash
# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy .

# Run all quality checks
poetry run black . && poetry run isort . && poetry run mypy .
```

4. **Building and Publishing**
```bash
# Build the package
poetry build

# Publish to PyPI (requires authentication)
poetry publish
```

## Usage

### Initialization

The SDK provides three ways to initialize the client:

1. Using client credentials (recommended for server-side applications):
```python
from payman_sdk import PaymanClient

payman = PaymanClient.with_credentials({
    'client_id': 'your-client-id',
    'client_secret': 'your-client-secret',
})
```

2. Using an authorization code (for OAuth flow):
```python
payman = PaymanClient.with_auth_code({
    'client_id': 'your-client-id',
    'environment': 'TEST'
}, 'your-auth-code')
```

3. Using an access token (when you already have a token):
```python
payman = PaymanClient.with_token(
    'your-client-id',
    {
        'access_token': 'your-access-token',
        'expires_in': 3600  # token expiry in seconds
    },
)
```

### Making Requests

1. Get a formatted response (recommended for most use cases):
```python
response = payman.ask("What's the weather?")
print(response)
```

2. Get a raw response (when you need the full JSON-RPC response):
```python
raw_response = payman.ask("What's the weather?", raw=True)
print(raw_response)
```

3. Streaming request with formatted responses:
```python
payman.ask("What's the weather?", {
    'on_message': lambda response: print(f"Formatted response: {response}")
})
```

4. Streaming request with raw responses:
```python
payman.ask("What's the weather?", {
    'on_message': lambda response: print(f"Raw response: {response}")
}, raw=True)
```

5. Start a new session with metadata:
```python
response = payman.ask("Hello!", {
    'new_session': True,
    'metadata': {'source': 'web-app'}
})
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `poetry run pytest`
5. Format code: `poetry run black . && poetry run isort .`
6. Check types: `poetry run mypy .`
7. Commit your changes: `git commit -am 'Add feature'`
8. Push to the branch: `git push origin feature-name`
9. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Testing

The SDK uses pytest for testing. To run the tests:

1. Make sure you have set up your `.env` file with the required credentials
2. Install dependencies:
```bash
pip install -e ".[dev]"
```
3. Run the tests:
```bash
pytest
```

The test suite will verify the SDK's functionality, including authentication, API interactions, and response handling.

## API Reference

### PaymanClient

#### Static Methods

- `with_credentials(config: PaymanConfig) -> PaymanClient`
  - Creates a client using client credentials
  - `config`: Configuration object containing client_id, client_secret, and optional environment

- `with_auth_code(config: PaymanConfig, auth_code: str) -> PaymanClient`
  - Creates a client using an authorization code
  - `config`: Configuration object containing client_id, client_secret, and optional environment
  - `auth_code`: Authorization code obtained via OAuth

- `with_token(client_id: str, token_info: Dict[str, Any], environment: Optional[Environment] = 'LIVE') -> PaymanClient`
  - Creates a client using an existing access token
  - `client_id`: Your Payman client ID
  - `token_info`: Object containing access token and its expiration time
  - `environment`: Optional environment to use (defaults to "LIVE")

#### Instance Methods

- `ask(text: str, options: Optional[AskOptions] = None, raw: bool = False) -> Union[FormattedTaskResponse, TaskResponse]`
  - Sends a message to the Payman AI Agent
  - `text`: The message or question to send
  - `options`: Optional parameters for the request
  - `raw`: Whether to return raw responses (default: False)

- `get_access_token() -> Optional[Dict[str, Any]]`
  - Gets the current access token and its expiration information
  - Returns None if no token is set

- `is_access_token_expired() -> bool`
  - Checks if the current access token has expired
  - Returns True if the token has expired or is about to expire within 60 seconds

### Types

- `PaymanConfig`
  ```python
  {
      'client_id': str,
      'client_secret': str,
      'environment': Optional[Literal['TEST', 'LIVE', 'INTERNAL']]
  }
  ```

- `AskOptions`
  ```python
  {
      'on_message': Optional[Callable[[Union[FormattedTaskResponse, TaskResponse]], None]],
      'new_session': Optional[bool],
      'metadata': Optional[Dict[str, Any]],
      'part_metadata': Optional[Dict[str, Any]],
      'message_metadata': Optional[Dict[str, Any]]
  }
  ```

### Response Types

- `FormattedTaskResponse`
  ```python
  {
      'status': Literal['completed', 'failed', 'in_progress'],
      'is_final': bool,
      'artifacts': Optional[List[Dict[str, Any]]],
      'error': Optional[Dict[str, Any]]
  }
  ```

- `TaskResponse`
  ```python
  {
      'jsonrpc': Literal['2.0'],
      'id': str,
      'result': Optional[Dict[str, Any]],
      'error': Optional[Dict[str, Any]]
  }
  ```

### Events

- `TaskStatusUpdateEvent`
  ```python
  {
      'type': Literal['status_update'],
      'status': Literal['completed', 'failed', 'in_progress'],
      'is_final': bool
  }
  ```

- `TaskArtifactUpdateEvent`
  ```python
  {
      'type': Literal['artifact_update'],
      'artifacts': List[Dict[str, Any]]
  }
  ```

## Error Handling

The SDK uses the `requests` library for HTTP requests. All API calls will raise an exception if the request fails. You can catch these exceptions and handle them appropriately:

```python
try:
    response = payman.ask("What's the weather?")
except requests.exceptions.RequestException as e:
    if hasattr(e, 'response'):
        # The request was made and the server responded with a status code
        # that falls out of the range of 2xx
        print(e.response.json())
        print(e.response.status_code)
    else:
        # Something happened in setting up the request that triggered an Error
        print('Error:', str(e)) 