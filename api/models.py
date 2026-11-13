from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class ModelInfo(BaseModel):
    """Model information response model."""
    
    id: str = Field(..., description="Model identifier")
    object: str = Field(default="model", description="Object type")
    created: int = Field(..., description="Creation timestamp")
    owned_by: str = Field(..., description="Organization that owns the model")
    description: Optional[str] = Field(None, description="Model description")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens for generation")
    context_window: Optional[int] = Field(None, description="Context window size")
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")
    capabilities: Optional[Dict[str, Any]] = Field(None, description="Model capabilities")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "gpt-4",
                "object": "model",
                "created": 1691961600,
                "owned_by": "openai",
                "description": "GPT-4 model for advanced tasks",
                "max_tokens": 8192,
                "context_window": 8192
            }
        }


class ProviderInfo(BaseModel):
    """Provider information model."""
    
    id: str = Field(..., description="Provider identifier")
    name: str = Field(..., description="Provider name")
    object: str = Field(default="provider", description="Object type")
    description: Optional[str] = Field(None, description="Provider description")
    models_available: Optional[int] = Field(None, description="Number of available models")
    is_active: bool = Field(default=True, description="Whether provider is active")
    health_status: Optional[str] = Field(None, description="Health status of provider")
    endpoint: Optional[str] = Field(None, description="Provider endpoint URL")
    capabilities: Optional[Dict[str, Any]] = Field(None, description="Provider capabilities")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "openai",
                "name": "OpenAI",
                "object": "provider",
                "description": "OpenAI's API for various models",
                "models_available": 50,
                "is_active": True,
                "health_status": "healthy",
                "endpoint": "https://api.openai.com/v1"
            }
        }


class KeyInfo(BaseModel):
    """API key information model."""
    
    id: str = Field(..., description="Key identifier")
    provider: str = Field(..., description="Provider this key belongs to")
    key_type: str = Field(..., description="Type of key (bearer, api_key, etc.)")
    is_active: bool = Field(default=True, description="Whether key is active")
    is_verified: bool = Field(default=False, description="Whether key has been verified")
    added_at: datetime = Field(default_factory=datetime.now, description="When key was added")
    last_used: Optional[datetime] = Field(None, description="Last usage timestamp")
    usage_count: int = Field(default=0, description="Number of times key has been used")
    status: str = Field(default="unknown", description="Status (healthy, issues, disabled)")
    priority: int = Field(default=1, description="Priority level for load balancing")
    quota_remaining: Optional[int] = Field(None, description="Remaining quota")
    quota_limit: Optional[int] = Field(None, description="Quota limit")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "key-123",
                "provider": "openai",
                "key_type": "bearer",
                "is_active": True,
                "is_verified": True,
                "added_at": "2026-11-13T08:25:03Z",
                "status": "healthy",
                "priority": 1,
                "quota_remaining": 1000000,
                "quota_limit": 1000000
            }
        }


class HealthInfo(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    providers_status: Optional[Dict[str, Any]] = Field(None, description="Provider status details")
    total_providers: Optional[int] = Field(None, description="Total number of providers")
    active_providers: Optional[int] = Field(None, description="Number of active providers")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-11-13T08:25:03Z",
                "version": "0.1.0",
                "providers_status": {"openai": "healthy", "anthropic": "healthy"},
                "total_providers": 87,
                "active_providers": 85
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Error type")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Provider not found",
                "error_type": "not_found",
                "details": {"provider_id": "nonexistent"}
            }
        }


class StatsResponse(BaseModel):
    """Statistics response model."""
    
    total_requests: int = Field(..., description="Total number of requests")
    successful_requests: int = Field(..., description="Successful requests")
    failed_requests: int = Field(..., description="Failed requests")
    providers_used: Optional[Dict[str, int]] = Field(None, description="Requests per provider")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_requests": 1000,
                "successful_requests": 985,
                "failed_requests": 15,
                "providers_used": {"openai": 500, "anthropic": 300, "custom": 200}
            }
        }


class CreateKeyRequest(BaseModel):
    """Request model for creating API keys."""
    
    provider: str = Field(..., description="Provider to associate key with")
    key: str = Field(..., description="API key value")
    key_type: str = Field(default="bearer", description="Type of key")
    priority: int = Field(default=1, description="Priority level")
    quota_limit: Optional[int] = Field(None, description="Quota limit for this key")
    tags: Optional[List[str]] = Field(None, description="Key tags for organization")
    
    class Config:
        json_schema_extra = {
            "example": {
                "provider": "openai",
                "key": "sk-test-key-1234567890abcdef",
                "key_type": "bearer",
                "priority": 1,
                "quota_limit": 1000000,
                "tags": ["production", "primary"]
            }
        }


class UpdateKeyRequest(BaseModel):
    """Request model for updating API keys."""
    
    is_active: Optional[bool] = Field(None, description="Whether key is active")
    priority: Optional[int] = Field(None, description="Priority level")
    quota_limit: Optional[int] = Field(None, description="New quota limit")
    status: Optional[str] = Field(None, description="Status (healthy, issues, disabled)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_active": True,
                "priority": 2,
                "status": "healthy"
            }
        }
