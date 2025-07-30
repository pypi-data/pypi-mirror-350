# FastAPI Comprehensive Demo

A complete demonstration of various FastAPI features, API types, and authentication methods.

## 🚀 Features

### API Types
- **REST API** - Standard HTTP endpoints with CRUD operations
- **WebSocket** - Real-time bidirectional communication
- **GraphQL** - Query language for APIs with Strawberry integration
- **File Upload/Download** - Async file handling
- **Server-Sent Events** - Real-time data streaming

### Authentication Methods
- **JWT (JSON Web Tokens)** - OAuth2 password flow with Bearer tokens
- **HTTP Basic Authentication** - Username/password with secure verification
- **API Key Authentication** - Multiple methods (header, query, cookie)
- **Custom Headers** - Custom authentication tokens

### Security Features
- **Password Hashing** - bcrypt with salt
- **Rate Limiting** - Request throttling (demo implementation)
- **CORS Configuration** - Cross-origin resource sharing
- **HTTPS Redirect** - Force secure connections
- **Trusted Host Middleware** - Host header validation
- **Custom Security Headers** - Additional security headers

### Advanced Features
- **Dependency Injection** - FastAPI's powerful DI system
- **Request/Response Middleware** - Custom processing pipeline
- **Database Integration Ready** - SQLAlchemy models included
- **Error Handling** - Comprehensive error responses
- **API Documentation** - Auto-generated OpenAPI/Swagger docs
- **Testing Support** - Comprehensive test client

## 📦 Installation

### Requirements

Create a `requirements.txt` file:

```txt
# Core FastAPI
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Database (Optional)
sqlalchemy==2.0.23
databases[aiosqlite]==0.8.0

# GraphQL
strawberry-graphql[fastapi]==0.214.1

# File Operations
aiofiles==23.2.1

# Configuration
python-decouple==3.8

# Testing
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1

# WebSocket Testing
websockets==12.0

# Additional utilities
requests-toolbelt==1.0.0
```

### Installation Steps

1. **Create virtual environment:**
   ```bash
   python -m venv fastapi_demo
   source fastapi_demo/bin/activate  # On Windows: fastapi_demo\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   # Or use uvicorn directly:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Run tests:**
   ```bash
   python test_client.py
   ```

## 🔧 Usage Examples

### 1. JWT Authentication Flow

```python
import httpx

async def jwt_example():
    async with httpx.AsyncClient() as client:
        # Get token
        response = await client.post(
            "http://localhost:8000/auth/token",
            data={"username": "testuser", "password": "secret"}
        )
        token = response.json()["access_token"]
        
        # Use token
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("http://localhost:8000/users/me", headers=headers)
        print(response.json())
```

### 2. HTTP Basic Authentication

```python
import base64
import httpx

async def basic_auth_example():
    credentials = base64.b64encode(b"testuser:secret").decode("ascii")
    headers = {"Authorization": f"Basic {credentials}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/users/me/basic", 
            headers=headers
        )
        print(response.json())
```

### 3. API Key Authentication

```python
import httpx

async def api_key_example():
    # Method 1: Header
    headers = {"X-API-Key": "super-secret-api-key"}
    
    # Method 2: Query parameter
    url = "http://localhost:8000/protected/api-key?api_key=super-secret-api-key"
    
    # Method 3: Cookie
    cookies = {"api_key": "super-secret-api-key"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/protected/api-key", 
            headers=headers
        )
        print(response.json())
```

### 4. WebSocket with Authentication

```python
import asyncio
import websockets

async def websocket_example():
    # With JWT token
    uri = "ws://localhost:8000/ws/123?token=YOUR_JWT_TOKEN"
    
    # Or with API key
    uri = "ws://localhost:8000/ws/123?api_key=super-secret-api-key"
    
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello WebSocket!")
        message = await websocket.recv()
        print(f"Received: {message}")

asyncio.run(websocket_example())
```

### 5. GraphQL Queries

```python
import httpx

async def graphql_example():
    query = {
        "query": """
        {
            hello
            items {
                id
                name
                price
            }
        }
        """
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/graphql", json=query)
        print(response.json())
```

### 6. File Upload

```python
import httpx

async def file_upload_example():
    # Get JWT token first
    token_response = await client.post(
        "http://localhost:8000/auth/token",
        data={"username": "testuser", "password": "secret"}
    )
    token = token_response.json()["access_token"]
    
    # Upload file
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": ("test.txt", b"Hello World!", "text/plain")}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/upload", 
            headers=headers, 
            files=files
        )
        print(response.json())
```

## 🔐 Default Credentials

### Users
- **Username:** `testuser` | **Password:** `secret`
- **Username:** `alice` | **Password:** `secret`

### API Keys
- **Admin:** `super-secret-api-key`
- **User:** `user-api-key`

### Custom Headers
- **X-Token:** `super-secret-token`

## 📚 API Endpoints

### Authentication
- `POST /auth/token` - Get JWT token
- `POST /auth/register` - Register new user

### Protected Endpoints
- `GET /users/me` - Get current user (JWT)
- `GET /users/me/basic` - Get current user (Basic Auth)
- `GET /protected/api-key` - Protected with API key
- `GET /protected/custom-header` - Protected with custom header

### CRUD Operations
- `GET /items` - List items (JWT required)
- `POST /items` - Create item (JWT required)
- `GET /items/{item_id}` - Get specific item (JWT required)

### File Operations
- `POST /upload` - Upload file (JWT required)
- `GET /download/{filename}` - Download file (JWT required)

### WebSocket
- `WS /ws/{client_id}` - WebSocket endpoint with auth

### GraphQL
- `POST /graphql` - GraphQL endpoint
- `GET /graphql` - GraphQL playground

### System
- `GET /health` - Health check
- `GET /metrics` - System metrics (API key required)
- `GET /rate-limited` - Rate limited endpoint
- `GET /chat` - WebSocket chat demo page

## 🧪 Testing

The demo includes a comprehensive test client that demonstrates all features:

```bash
python test_client.py
```

Or test specific features:

```python
async with FastAPITestClient() as client:
    await client.test_jwt_authentication()
    await client.test_websocket_with_jwt()
    await client.test_graphql()
```

## 🌐 Interactive Documentation

Once running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc  
- **GraphQL Playground:** http://localhost:8000/graphql
- **WebSocket Chat Demo:** http://localhost:8000/chat

## 🔒 Security Notes

This is a **DEMO APPLICATION** for learning purposes. For production use:

1. **Change all default secrets and keys**
2. **Use environment variables for configuration**
3. **Implement proper database with connection pooling**
4. **Add proper logging and monitoring**
5. **Use Redis or similar for rate limiting**
6. **Enable HTTPS and security headers**
7. **Implement proper session management**
8. **Add input validation and sanitization**
9. **Use proper error handling without exposing internal details**
10. **Add comprehensive testing and CI/CD**

## 🏗️ Architecture Overview

```
FastAPI Application
├── Authentication Layer
│   ├── JWT (OAuth2 Password Bearer)
│   ├── HTTP Basic Auth
│   ├── API Key (Header/Query/Cookie)
│   └── Custom Headers
├── API Layer
│   ├── REST Endpoints
│   ├── WebSocket Endpoints
│   ├── GraphQL Endpoints
│   └── File Operations
├── Middleware Layer
│   ├── CORS
│   ├── Security Headers
│   ├── Rate Limiting
│   └── Request Timing
├── Data Layer
│   ├── In-Memory Storage (Demo)
│   └── SQLAlchemy Models (Ready)
└── Testing Layer
    ├── Comprehensive Test Client
    └── Interactive Documentation
```

## 🤝 Contributing

This is a demo application, but improvements are welcome! Areas for enhancement:

- Add more authentication methods (OAuth2 with external providers)
- Implement database operations with real persistence
- Add more middleware examples
- Enhance error handling and validation
- Add more comprehensive testing examples
- Implement background tasks
- Add caching examples
- Include monitoring and metrics

## 📄 License

This demo is provided as-is for educational purposes. Use at your own risk and always review security implications before using any code in production.