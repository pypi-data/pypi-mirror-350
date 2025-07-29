# AuthFlow Python SDK

The official Python SDK for AuthFlow - drop-in authentication for any application.

[![PyPI version](https://badge.fury.io/py/authflow.svg)](https://badge.fury.io/py/authflow)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/authflow.svg)](https://pypi.org/project/authflow/)

## Installation

```bash
pip install authflow
```

## Quick Start

```python
from authflow import AuthFlowClient

# Initialize the client
client = AuthFlowClient(
    api_key="your-api-key-here",
    base_url="https://your-authflow-instance.com/api"
)

# Authenticate a user
auth_response = client.authenticate_user(
    application_id=1,
    email="user@example.com",
    password="password123"
)

print(f"Authentication successful: {auth_response['user']}")
```

## Features

- ✅ **Complete Authentication** - Email/password, OAuth, MFA support
- ✅ **User Management** - Registration, profiles, roles
- ✅ **API Key Management** - Generate, validate, revoke keys
- ✅ **Application Management** - Multi-tenant application support
- ✅ **Analytics** - Usage tracking and insights
- ✅ **Framework Support** - Flask, Django, FastAPI compatible

## Framework Examples

### Flask

```python
from flask import Flask, request, jsonify
from authflow import AuthFlowClient
import os

app = Flask(__name__)

# Initialize AuthFlow client
client = AuthFlowClient(
    api_key=os.getenv('AUTHFLOW_API_KEY'),
    base_url=os.getenv('AUTHFLOW_BASE_URL')
)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        user = client.register_user(
            application_id=1,
            email=data['email'],
            password=data['password'],
            user_data={
                'first_name': data.get('firstName'),
                'last_name': data.get('lastName')
            }
        )
        
        return jsonify({'success': True, 'user': user})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        auth_response = client.authenticate_user(
            application_id=1,
            email=data['email'],
            password=data['password']
        )
        
        return jsonify({
            'success': True,
            'token': auth_response['token'],
            'user': auth_response['user']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)
```

### Django

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from authflow import AuthFlowClient
import json
import os

# Initialize AuthFlow client
client = AuthFlowClient(
    api_key=os.getenv('AUTHFLOW_API_KEY'),
    base_url=os.getenv('AUTHFLOW_BASE_URL')
)

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
        
        user = client.register_user(
            application_id=1,
            email=data['email'],
            password=data['password'],
            user_data={
                'first_name': data.get('firstName'),
                'last_name': data.get('lastName')
            }
        )
        
        return JsonResponse({'success': True, 'user': user})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        
        auth_response = client.authenticate_user(
            application_id=1,
            email=data['email'],
            password=data['password']
        )
        
        return JsonResponse({
            'success': True,
            'token': auth_response['token'],
            'user': auth_response['user']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=401)
```

### FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from authflow import AuthFlowClient
import os

app = FastAPI()

# Initialize AuthFlow client
client = AuthFlowClient(
    api_key=os.getenv('AUTHFLOW_API_KEY'),
    base_url=os.getenv('AUTHFLOW_BASE_URL')
)

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str = None
    last_name: str = None

@app.post("/register")
async def register(request: RegisterRequest):
    try:
        user = client.register_user(
            application_id=1,
            email=request.email,
            password=request.password,
            user_data={
                'first_name': request.first_name,
                'last_name': request.last_name
            }
        )
        return {"success": True, "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
async def login(request: LoginRequest):
    try:
        auth_response = client.authenticate_user(
            application_id=1,
            email=request.email,
            password=request.password
        )
        return {
            "success": True,
            "token": auth_response['token'],
            "user": auth_response['user']
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
```

## API Reference

### Client Initialization

```python
from authflow import AuthFlowClient

client = AuthFlowClient(
    api_key="your-api-key",
    base_url="https://api.authflow.com"  # optional
)
```

### Authentication Methods

#### `authenticate_user(application_id, email, password)`

Authenticate a user with email and password credentials.

```python
response = client.authenticate_user(1, "user@example.com", "password")
# Returns: {"token": str, "user": dict}
```

#### `register_user(application_id, email, password, user_data=None)`

Register a new user with optional additional data.

```python
user = client.register_user(
    application_id=1,
    email="user@example.com",
    password="password",
    user_data={
        "first_name": "John",
        "last_name": "Doe"
    }
)
```

### User Management

#### `get_user(user_id)`

Retrieve user information by user ID.

```python
user = client.get_user("user-id-123")
```

### Application Management

#### `get_applications()`

Get all applications for the authenticated user.

```python
applications = client.get_applications()
```

#### `create_application(name, options=None)`

Create a new application.

```python
app = client.create_application("My App", {
    "description": "My awesome application",
    "domain": "myapp.com"
})
```

### API Key Management

#### `get_api_keys()`

Retrieve all API keys.

```python
api_keys = client.get_api_keys()
```

#### `create_api_key(name, application_id=None)`

Create a new API key.

```python
api_key = client.create_api_key("Production Key", application_id=1)
```

### Analytics

#### `get_analytics(start_date=None, end_date=None)`

Get usage analytics for a date range.

```python
from datetime import datetime

analytics = client.get_analytics(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 1, 31)
)
```

## Error Handling

The SDK raises descriptive exceptions that you can catch and handle:

```python
from authflow import AuthFlowClient, AuthFlowException

client = AuthFlowClient(api_key="your-key")

try:
    auth = client.authenticate_user(1, "user@example.com", "wrong-password")
except AuthFlowException as e:
    if "Invalid credentials" in str(e):
        # Handle authentication failure
        pass
    elif "Rate limit" in str(e):
        # Handle rate limiting
        pass
    else:
        # Handle other errors
        pass
```

## Configuration

You can configure the client with environment variables:

```bash
export AUTHFLOW_API_KEY="your-api-key"
export AUTHFLOW_BASE_URL="https://your-instance.authflow.com/api"
```

```python
import os
from authflow import AuthFlowClient

# Client will automatically use environment variables
client = AuthFlowClient()
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📚 [Documentation](https://docs.authflow.com)
- 💬 [Discord Community](https://discord.gg/authflow)
- 📧 [Email Support](mailto:support@authflow.com)
- 🐛 [Report Issues](https://github.com/authflow/sdk-python/issues)

## Related Projects

- [AuthFlow Node.js SDK](https://github.com/authflow/sdk-nodejs)
- [AuthFlow Go SDK](https://github.com/authflow/sdk-go)
- [AuthFlow React Components](https://github.com/authflow/react-components)