"""
Comprehensive FastAPI Demo Application
=====================================

This demo showcases various API types and authentication methods:
- REST API endpoints with different auth methods
- WebSocket connections with authentication
- GraphQL integration
- File upload/download
- Various middleware configurations
- Database integration with SQLAlchemy
- JWT, OAuth2, HTTP Basic, API Key authentication
- CORS, rate limiting, and security headers

Requirements:
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart
pip install sqlalchemy databases[aiosqlite] strawberry-graphql aiofiles python-decouple
"""

import os
import time
import secrets
from datetime import datetime, timedelta
from typing import List, Optional, Annotated
from pathlib import Path

import strawberry
from fastapi import (
    FastAPI, Depends, HTTPException, status, Header, Cookie, Query, 
    Path as PathParam, File, UploadFile, WebSocket, WebSocketDisconnect,
    Request, Response, Security
)
from fastapi.security import (
    OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, 
    HTTPBasicCredentials, APIKeyHeader, APIKeyCookie, APIKeyQuery
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from strawberry.fastapi import GraphQLRouter
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
import aiofiles

# ========================
# Configuration & Setup
# ========================

app = FastAPI(
    title="Comprehensive API Demo",
    description="Demo showcasing various API types and authentication methods",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ========================
# Middleware Configuration
# ========================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (uncomment in production)
# app.add_middleware(
#     TrustedHostMiddleware, 
#     allowed_hosts=["example.com", "*.example.com"]
# )

# HTTPS Redirect Middleware (uncomment in production)
# app.add_middleware(HTTPSRedirectMiddleware)

# Custom middleware for request timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Custom-Header"] = "FastAPI-Demo"
    return response

# ========================
# Data Models
# ========================

class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    owner: Optional[str] = None

class Message(BaseModel):
    message: str
    timestamp: datetime = datetime.now()
    user: Optional[str] = None

# ========================
# Fake Database
# ========================

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Smith",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "disabled": False,
    }
}

fake_items_db = [
    {"id": 1, "name": "Laptop", "description": "Gaming laptop", "price": 999.99, "owner": "testuser"},
    {"id": 2, "name": "Mouse", "description": "Wireless mouse", "price": 29.99, "owner": "alice"},
]

# API Keys for demo
VALID_API_KEYS = {
    "super-secret-api-key": "admin",
    "user-api-key": "user"
}

# ========================
# Authentication Setup
# ========================

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# HTTP Basic Auth
security_basic = HTTPBasic()

# API Key Authentication (multiple methods)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_cookie = APIKeyCookie(name="api_key", auto_error=False)

# ========================
# Authentication Functions
# ========================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ========================
# Dependency Functions
# ========================

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_user_basic(credentials: Annotated[HTTPBasicCredentials, Depends(security_basic)]):
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")
    
    user = get_user(fake_users_db, credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    api_key = api_key_query or api_key_header or api_key_cookie
    if api_key and api_key in VALID_API_KEYS:
        return {"api_key": api_key, "user": VALID_API_KEYS[api_key]}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key"
    )

# Custom header dependency
async def get_custom_header(x_token: Annotated[str, Header()]):
    if x_token != "super-secret-token":
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    return x_token

# ========================
# Authentication Endpoints
# ========================

@app.post("/auth/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """OAuth2 Password flow - get access token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/register", response_model=User, tags=["Authentication"])
async def register_user(user: User, password: str):
    """Register a new user"""
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    fake_users_db[user.username] = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "hashed_password": get_password_hash(password),
        "disabled": False,
    }
    return user

# ========================
# Protected Endpoints (Different Auth Methods)
# ========================

@app.get("/users/me", response_model=User, tags=["Users"])
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """Get current user info (JWT Auth)"""
    return current_user

@app.get("/users/me/basic", response_model=User, tags=["Users"])
async def read_users_me_basic(current_user: Annotated[User, Depends(get_current_user_basic)]):
    """Get current user info (HTTP Basic Auth)"""
    return current_user

@app.get("/protected/api-key", tags=["Protected"])
async def protected_api_key(api_key_info: dict = Depends(get_api_key)):
    """Protected endpoint using API Key (query, header, or cookie)"""
    return {"message": "Access granted", "user": api_key_info["user"]}

@app.get("/protected/custom-header", tags=["Protected"])
async def protected_custom_header(token: str = Depends(get_custom_header)):
    """Protected endpoint using custom header"""
    return {"message": "Access granted with custom header", "token": token}

# ========================
# CRUD Operations with Different Auth
# ========================

@app.get("/items", response_model=List[Item], tags=["Items"])
async def read_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100
):
    """Get items for current user (JWT Auth)"""
    user_items = [item for item in fake_items_db if item["owner"] == current_user.username]
    return user_items[skip : skip + limit]

@app.post("/items", response_model=Item, tags=["Items"])
async def create_item(
    item: Item,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Create new item (JWT Auth)"""
    item.owner = current_user.username
    item.id = len(fake_items_db) + 1
    fake_items_db.append(item.dict())
    return item

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def read_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Get specific item (JWT Auth)"""
    for item in fake_items_db:
        if item["id"] == item_id and item["owner"] == current_user.username:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# ========================
# File Upload/Download
# ========================

# Create uploads directory
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)

@app.post("/upload", tags=["Files"])
async def upload_file(
    current_user: Annotated[User, Depends(get_current_active_user)],
    file: UploadFile = File(...)
):
    """Upload file (JWT Auth required)"""
    file_path = uploads_dir / f"{current_user.username}_{file.filename}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "path": str(file_path)
    }

@app.get("/download/{filename}", tags=["Files"])
async def download_file(
    filename: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Download file (JWT Auth required)"""
    file_path = uploads_dir / f"{current_user.username}_{filename}"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

# ========================
# WebSocket with Authentication
# ========================

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[dict] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections.append({"websocket": websocket, "user": user})

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [
            conn for conn in self.active_connections 
            if conn["websocket"] != websocket
        ]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection["websocket"].send_text(message)

manager = ConnectionManager()

async def get_websocket_user(
    websocket: WebSocket,
    token: Annotated[Optional[str], Query()] = None,
    api_key: Annotated[Optional[str], Query()] = None
):
    """Authenticate WebSocket connection"""
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username and username in fake_users_db:
                return username
        except JWTError:
            pass
    
    if api_key and api_key in VALID_API_KEYS:
        return VALID_API_KEYS[api_key]
    
    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return None

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    user: Annotated[str, Depends(get_websocket_user)]
):
    """WebSocket endpoint with authentication"""
    await manager.connect(websocket, user)
    await manager.send_personal_message(f"Welcome {user}! Client ID: {client_id}", websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = f"User {user} (Client {client_id}): {data}"
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User {user} (Client {client_id}) left the chat")

# ========================
# GraphQL Integration
# ========================

@strawberry.type
class ItemType:
    id: int
    name: str
    description: Optional[str]
    price: float
    owner: str

@strawberry.type
class UserType:
    username: str
    full_name: Optional[str]
    email: Optional[str]

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World from GraphQL!"
    
    @strawberry.field
    def items(self) -> List[ItemType]:
        return [
            ItemType(
                id=item["id"],
                name=item["name"],
                description=item["description"],
                price=item["price"],
                owner=item["owner"]
            )
            for item in fake_items_db
        ]
    
    @strawberry.field
    def users(self) -> List[UserType]:
        return [
            UserType(
                username=user["username"],
                full_name=user["full_name"],
                email=user["email"]
            )
            for user in fake_users_db.values()
        ]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_item(self, name: str, price: float, description: Optional[str] = None) -> ItemType:
        new_item = {
            "id": len(fake_items_db) + 1,
            "name": name,
            "description": description,
            "price": price,
            "owner": "graphql_user"
        }
        fake_items_db.append(new_item)
        return ItemType(**new_item)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql", tags=["GraphQL"])

# ========================
# Health Check & Metrics
# ========================

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/metrics", tags=["System"])
async def get_metrics(api_key_info: dict = Depends(get_api_key)):
    """Get system metrics (API Key required)"""
    return {
        "total_users": len(fake_users_db),
        "total_items": len(fake_items_db),
        "active_connections": len(manager.active_connections),
        "uptime": "unknown"  # In real app, calculate actual uptime
    }

# ========================
# Rate Limited Endpoint
# ========================

# Simple in-memory rate limiting (use Redis in production)
request_counts = {}

@app.get("/rate-limited", tags=["System"])
async def rate_limited_endpoint(request: Request):
    """Rate limited endpoint (demo implementation)"""
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    
    # Clean old requests (older than 1 minute)
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip]
        if current_time - req_time < 60
    ]
    
    # Check rate limit (10 requests per minute)
    if len(request_counts[client_ip]) >= 10:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    request_counts[client_ip].append(current_time)
    return {"message": "Request successful", "remaining": 10 - len(request_counts[client_ip])}

# ========================
# HTML Response for WebSocket Testing
# ========================

@app.get("/chat", response_class=HTMLResponse, tags=["Frontend"])
async def get_chat_page():
    """Simple chat page for WebSocket testing"""
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>WebSocket Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat Demo</h1>
            <div>
                <label>Token (JWT): <input type="text" id="token" placeholder="Get from /auth/token"></label><br><br>
                <label>Or API Key: <input type="text" id="apikey" placeholder="super-secret-api-key"></label><br><br>
                <label>Client ID: <input type="number" id="clientId" value="123"></label><br><br>
                <button onclick="connect()">Connect</button>
                <button onclick="disconnect()">Disconnect</button>
            </div>
            <div>
                <input type="text" id="messageText" placeholder="Type message here..." />
                <button onclick="sendMessage()">Send</button>
            </div>
            <ul id="messages"></ul>
            
            <script>
                let ws = null;
                
                function connect() {
                    const token = document.getElementById('token').value;
                    const apikey = document.getElementById('apikey').value;
                    const clientId = document.getElementById('clientId').value;
                    
                    let wsUrl = `ws://localhost:8000/ws/${clientId}`;
                    if (token) wsUrl += `?token=${token}`;
                    else if (apikey) wsUrl += `?api_key=${apikey}`;
                    
                    ws = new WebSocket(wsUrl);
                    ws.onmessage = function(event) {
                        const messages = document.getElementById('messages');
                        const message = document.createElement('li');
                        message.textContent = event.data;
                        messages.appendChild(message);
                    };
                    ws.onopen = function() {
                        console.log('Connected');
                    };
                    ws.onclose = function() {
                        console.log('Disconnected');
                    };
                }
                
                function disconnect() {
                    if (ws) ws.close();
                }
                
                function sendMessage() {
                    const input = document.getElementById('messageText');
                    if (ws && input.value) {
                        ws.send(input.value);
                        input.value = '';
                    }
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

# ========================
# Startup Event
# ========================

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("🚀 FastAPI Comprehensive Demo Started!")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 GraphQL Playground: http://localhost:8000/graphql")
    print("💬 WebSocket Chat: http://localhost:8000/chat")
    print("\n🔐 Authentication Methods Available:")
    print("  - JWT Token: POST /auth/token (username: testuser, password: secret)")
    print("  - HTTP Basic: Use testuser:secret")
    print("  - API Key: super-secret-api-key (header: X-API-Key or query: api_key)")
    print("  - Custom Header: X-Token: super-secret-token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)