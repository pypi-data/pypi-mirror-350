"""
FastAPI Demo Test Client
========================

This script demonstrates how to interact with all the different API endpoints
and authentication methods in the FastAPI demo application.

Requirements:
pip install httpx websockets requests-toolbelt
"""

import asyncio
import json
import base64
from pathlib import Path
import httpx
import websockets
from typing import Optional

class FastAPITestClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
        self.token: Optional[str] = None
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def print_response(self, title: str, response: httpx.Response):
        """Pretty print API response"""
        print(f"\n{'='*50}")
        print(f"🔍 {title}")
        print(f"{'='*50}")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        try:
            content = response.json()
            print(f"Response: {json.dumps(content, indent=2)}")
        except:
            print(f"Response: {response.text}")

    async def test_health_check(self):
        """Test basic health check endpoint"""
        response = await self.client.get("/health")
        self.print_response("Health Check", response)

    async def test_jwt_authentication(self):
        """Test JWT token authentication flow"""
        print(f"\n{'🔐 JWT AUTHENTICATION FLOW' : ^60}")
        
        # 1. Get access token
        token_data = {
            "username": "testuser",
            "password": "secret"
        }
        response = await self.client.post("/auth/token", data=token_data)
        self.print_response("Get JWT Token", response)
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            
            # 2. Use token to access protected endpoint
            headers = {"Authorization": f"Bearer {self.token}"}
            response = await self.client.get("/users/me", headers=headers)
            self.print_response("Get Current User (JWT)", response)
            
            # 3. Create an item
            item_data = {
                "name": "Test Laptop",
                "description": "A test laptop",
                "price": 1299.99,
                "tax": 129.99
            }
            response = await self.client.post("/items", json=item_data, headers=headers)
            self.print_response("Create Item (JWT)", response)
            
            # 4. Get items
            response = await self.client.get("/items", headers=headers)
            self.print_response("Get Items (JWT)", response)

    async def test_basic_authentication(self):
        """Test HTTP Basic authentication"""
        print(f"\n{'🔐 HTTP BASIC AUTHENTICATION' : ^60}")
        
        # Create basic auth header
        credentials = base64.b64encode(b"testuser:secret").decode("ascii")
        headers = {"Authorization": f"Basic {credentials}"}
        
        response = await self.client.get("/users/me/basic", headers=headers)
        self.print_response("Get Current User (Basic Auth)", response)

    async def test_api_key_authentication(self):
        """Test API Key authentication (header, query, cookie)"""
        print(f"\n{'🔐 API KEY AUTHENTICATION' : ^60}")
        
        api_key = "super-secret-api-key"
        
        # 1. API Key in header
        headers = {"X-API-Key": api_key}
        response = await self.client.get("/protected/api-key", headers=headers)
        self.print_response("API Key in Header", response)
        
        # 2. API Key in query parameter
        response = await self.client.get(f"/protected/api-key?api_key={api_key}")
        self.print_response("API Key in Query", response)
        
        # 3. API Key in cookie
        cookies = {"api_key": api_key}
        response = await self.client.get("/protected/api-key", cookies=cookies)
        self.print_response("API Key in Cookie", response)

    async def test_custom_header_auth(self):
        """Test custom header authentication"""
        print(f"\n{'🔐 CUSTOM HEADER AUTHENTICATION' : ^60}")
        
        headers = {"X-Token": "super-secret-token"}
        response = await self.client.get("/protected/custom-header", headers=headers)
        self.print_response("Custom Header Auth", response)

    async def test_file_operations(self):
        """Test file upload and download"""
        print(f"\n{'📁 FILE OPERATIONS' : ^60}")
        
        if not self.token:
            await self.test_jwt_authentication()
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Create a test file
        test_file_content = b"This is a test file for upload/download demo."
        test_file_name = "test_file.txt"
        
        # Upload file
        files = {"file": (test_file_name, test_file_content, "text/plain")}
        response = await self.client.post("/upload", headers=headers, files=files)
        self.print_response("File Upload", response)
        
        # Download file
        response = await self.client.get(f"/download/{test_file_name}", headers=headers)
        self.print_response("File Download", response)

    async def test_graphql(self):
        """Test GraphQL endpoints"""
        print(f"\n{'🔄 GRAPHQL QUERIES' : ^60}")
        
        # GraphQL Query
        query = {
            "query": """
            {
                hello
                items {
                    id
                    name
                    price
                    owner
                }
                users {
                    username
                    fullName
                    email
                }
            }
            """
        }
        
        response = await self.client.post("/graphql", json=query)
        self.print_response("GraphQL Query", response)
        
        # GraphQL Mutation
        mutation = {
            "query": """
            mutation {
                addItem(name: "GraphQL Item", price: 99.99, description: "Created via GraphQL") {
                    id
                    name
                    price
                    description
                    owner
                }
            }
            """
        }
        
        response = await self.client.post("/graphql", json=mutation)
        self.print_response("GraphQL Mutation", response)

    async def test_rate_limiting(self):
        """Test rate limiting endpoint"""
        print(f"\n{'⏱️ RATE LIMITING TEST' : ^60}")
        
        # Send multiple requests to trigger rate limit
        for i in range(12):  # Limit is 10 per minute
            response = await self.client.get("/rate-limited")
            if response.status_code == 429:
                self.print_response(f"Rate Limited Request #{i+1}", response)
                break
            elif i < 3 or i >= 9:  # Print first few and last few
                self.print_response(f"Request #{i+1}", response)

    async def test_websocket_with_jwt(self):
        """Test WebSocket connection with JWT authentication"""
        print(f"\n{'🔌 WEBSOCKET WITH JWT' : ^60}")
        
        if not self.token:
            await self.test_jwt_authentication()
        
        uri = f"ws://localhost:8000/ws/123?token={self.token}"
        
        try:
            async with websockets.connect(uri) as websocket:
                print("✅ WebSocket connected with JWT token")
                
                # Send a message
                await websocket.send("Hello from test client!")
                
                # Receive messages for a short time
                try:
                    for _ in range(3):
                        message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        print(f"📨 Received: {message}")
                except asyncio.TimeoutError:
                    print("⏰ No more messages received")
                    
        except Exception as e:
            print(f"❌ WebSocket connection failed: {e}")

    async def test_websocket_with_api_key(self):
        """Test WebSocket connection with API key"""
        print(f"\n{'🔌 WEBSOCKET WITH API KEY' : ^60}")
        
        uri = "ws://localhost:8000/ws/456?api_key=super-secret-api-key"
        
        try:
            async with websockets.connect(uri) as websocket:
                print("✅ WebSocket connected with API key")
                
                # Send a message
                await websocket.send("Hello from API key client!")
                
                # Receive messages for a short time
                try:
                    for _ in range(3):
                        message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        print(f"📨 Received: {message}")
                except asyncio.TimeoutError:
                    print("⏰ No more messages received")
                    
        except Exception as e:
            print(f"❌ WebSocket connection failed: {e}")

    async def test_metrics_endpoint(self):
        """Test metrics endpoint with API key"""
        print(f"\n{'📊 SYSTEM METRICS' : ^60}")
        
        headers = {"X-API-Key": "super-secret-api-key"}
        response = await self.client.get("/metrics", headers=headers)
        self.print_response("System Metrics", response)

    async def test_user_registration(self):
        """Test user registration"""
        print(f"\n{'👤 USER REGISTRATION' : ^60}")
        
        new_user = {
            "username": "newuser",
            "email": "newuser@example.com",
            "full_name": "New User"
        }
        
        # Register new user
        response = await self.client.post(
            "/auth/register", 
            json={**new_user, "password": "newpassword"}
        )
        self.print_response("User Registration", response)

    async def test_error_scenarios(self):
        """Test various error scenarios"""
        print(f"\n{'❌ ERROR SCENARIOS' : ^60}")
        
        # 1. Invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = await self.client.get("/users/me", headers=headers)
        self.print_response("Invalid JWT Token", response)
        
        # 2. Missing API key
        response = await self.client.get("/protected/api-key")
        self.print_response("Missing API Key", response)
        
        # 3. Invalid credentials
        invalid_credentials = base64.b64encode(b"invalid:invalid").decode("ascii")
        headers = {"Authorization": f"Basic {invalid_credentials}"}
        response = await self.client.get("/users/me/basic", headers=headers)
        self.print_response("Invalid Basic Auth", response)
        
        # 4. Invalid custom header
        headers = {"X-Token": "invalid-token"}
        response = await self.client.get("/protected/custom-header", headers=headers)
        self.print_response("Invalid Custom Header", response)

    async def run_all_tests(self):
        """Run all tests"""
        print("🧪 Starting FastAPI Comprehensive Demo Tests")
        print("=" * 60)
        
        await self.test_health_check()
        await self.test_jwt_authentication()
        await self.test_basic_authentication()
        await self.test_api_key_authentication()
        await self.test_custom_header_auth()
        await self.test_file_operations()
        await self.test_graphql()
        await self.test_user_registration()
        await self.test_metrics_endpoint()
        await self.test_rate_limiting()
        await self.test_error_scenarios()
        
        # WebSocket tests (require asyncio event loop)
        await self.test_websocket_with_jwt()
        await self.test_websocket_with_api_key()
        
        print(f"\n{'✅ ALL TESTS COMPLETED' : ^60}")
        print("🔗 Visit http://localhost:8000/docs for interactive API documentation")
        print("🔄 Visit http://localhost:8000/graphql for GraphQL playground")
        print("💬 Visit http://localhost:8000/chat for WebSocket chat demo")

async def main():
    """Main function to run all tests"""
    async with FastAPITestClient() as client:
        await client.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())