"""
Basic unit tests for axiom-console-145 API.
"""

import pytest
from fastapi.testclient import TestClient
from api import create_app


class TestAPI:
    """Test API endpoints and functionality."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app = create_app()
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "axiom-console-145 API"
        assert "endpoints" in data
        assert len(data["endpoints"]) > 0
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
    
    def test_health_stats_endpoint(self, client):
        """Test health stats endpoint."""
        response = client.get("/v1/health/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_requests" in data
        assert "successful_requests" in data
        assert "failed_requests" in data
    
    def test_models_endpoint(self, client):
        """Test models endpoint."""
        response = client.get("/v1/models")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check first model structure
        if data:
            model = data[0]
            assert "id" in model
            assert "owned_by" in model
            assert "object" in model
    
    def test_providers_endpoint(self, client):
        """Test providers endpoint."""
        response = client.get("/v1/models/providers")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check first provider structure
        if data:
            provider = data[0]
            assert "id" in provider
            assert "name" in provider
            assert "object" in provider
    
    def test_keys_endpoint_empty(self, client):
        """Test keys endpoint with no existing keys."""
        response = client.get("/v1/keys")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Initially should be empty since we use in-memory storage
        assert len(data) == 0
    
    def test_create_key(self, client):
        """Test creating a new API key."""
        key_data = {
            "provider": "test-provider",
            "key": "test-key-12345",
            "key_type": "bearer",
            "priority": 1,
            "quota_limit": 1000000
        }
        
        response = client.post("/v1/keys", json=key_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["provider"] == key_data["provider"]
        assert data["key_type"] == key_data["key_type"]
        assert data["priority"] == key_data["priority"]
        assert data["status"] == "healthy"
        assert "id" in data
        assert "added_at" in data
    
    def test_get_specific_key(self, client):
        """Test getting a specific key after creation."""
        # First create a key
        key_data = {
            "provider": "test-provider",
            "key": "test-key-67890",
            "key_type": "api_key"
        }
        
        create_response = client.post("/v1/keys", json=key_data)
        assert create_response.status_code == 200
        created_key = create_response.json()
        key_id = created_key["id"]
        
        # Now retrieve it
        get_response = client.get(f"/v1/keys/{key_id}")
        
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == key_id
        assert data["provider"] == key_data["provider"]
        assert data["key_type"] == key_data["key_type"]
    
    def test_update_key(self, client):
        """Test updating an existing key."""
        # Create a key first
        key_data = {
            "provider": "test-provider",
            "key": "test-key-update",
            "key_type": "bearer"
        }
        
        create_response = client.post("/v1/keys", json=key_data)
        assert create_response.status_code == 200
        created_key = create_response.json()
        key_id = created_key["id"]
        
        # Update the key
        update_data = {
            "is_active": False,
            "priority": 3,
            "status": "disabled"
        }
        
        update_response = client.put(f"/v1/keys/{key_id}", json=update_data)
        
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["id"] == key_id
        assert data["is_active"] == False
        assert data["priority"] == 3
        assert data["status"] == "disabled"
    
    def test_delete_key(self, client):
        """Test deleting a key."""
        # Create a key first
        key_data = {
            "provider": "test-provider",
            "key": "test-key-delete",
            "key_type": "bearer"
        }
        
        create_response = client.post("/v1/keys", json=key_data)
        assert create_response.status_code == 200
        created_key = create_response.json()
        key_id = created_key["id"]
        
        # Delete the key
        delete_response = client.delete(f"/v1/keys/{key_id}")
        
        assert delete_response.status_code == 200
        delete_data = delete_response.json()
        assert "message" in delete_data
        assert key_id in delete_data["message"]
        
        # Verify it's gone
        get_response = client.get(f"/v1/keys/{key_id}")
        assert get_response.status_code == 404
    
    def test_key_filtering(self, client):
        """Test key filtering functionality."""
        # Create keys with different properties
        keys_data = [
            {
                "provider": "openai",
                "key": "key-1",
                "key_type": "bearer",
                "priority": 1,
                "status": "healthy"
            },
            {
                "provider": "anthropic", 
                "key": "key-2",
                "key_type": "api_key",
                "priority": 2,
                "status": "issues"
            },
            {
                "provider": "openai",
                "key": "key-3", 
                "key_type": "bearer",
                "priority": 1,
                "status": "healthy"
            }
        ]
        
        # Create all keys
        for key_data in keys_data:
            response = client.post("/v1/keys", json=key_data)
            assert response.status_code == 200
        
        # Test provider filtering
        response = client.get("/v1/keys?provider=openai")
        assert response.status_code == 200
        openai_keys = response.json()
        assert len(openai_keys) == 2
        for key in openai_keys:
            assert key["provider"] == "openai"
        
        # Test status filtering
        response = client.get("/v1/keys?status=healthy")
        assert response.status_code == 200
        healthy_keys = response.json()
        assert len(healthy_keys) == 2
        for key in healthy_keys:
            assert key["status"] == "healthy"
