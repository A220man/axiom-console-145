from fastapi import HTTPException, APIRouter
from ..models import KeyInfo, CreateKeyRequest, UpdateKeyRequest
from datetime import datetime
import uuid
from typing import List, Optional, Dict

# Create router
router = APIRouter()

# In-memory storage for API keys
keys_db: Dict[str, KeyInfo] = {}

@router.get("/", response_model=list[KeyInfo])
async def get_keys(
    provider: Optional[str] = None,
    status: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get API keys with optional filtering."""
    
    keys = list(keys_db.values())
    
    # Apply filters
    if provider:
        keys = [k for k in keys if k.provider == provider]
    if status:
        keys = [k for k in keys if k.status == status]
    if is_active is not None:
        keys = [k for k in keys if k.is_active == is_active]
    
    return keys

@router.get("/{key_id}", response_model=KeyInfo)
async def get_key(key_id: str):
    """Get a specific API key by ID."""
    
    if key_id not in keys_db:
        raise HTTPException(status_code=404, detail=f"Key not found: {key_id}")
    
    return keys_db[key_id]

@router.post("/", response_model=KeyInfo)
async def create_key(key_request: CreateKeyRequest):
    """Create a new API key."""
    
    key_id = str(uuid.uuid4())
    
    key_info = KeyInfo(
        id=key_id,
        provider=key_request.provider,
        key_type=key_request.key_type,
        is_active=True,
        added_at=datetime.now(),
        status="healthy",
        priority=key_request.priority,
        quota_remaining=key_request.quota_limit,
        quota_limit=key_request.quota_limit
    )
    
    keys_db[key_id] = key_info
    
    return key_info

@router.put("/{key_id}", response_model=KeyInfo)
async def update_key(key_id: str, key_request: UpdateKeyRequest):
    """Update an existing API key."""
    
    if key_id not in keys_db:
        raise HTTPException(status_code=404, detail=f"Key not found: {key_id}")
    
    key_info = keys_db[key_id]
    
    if key_request.is_active is not None:
        key_info.is_active = key_request.is_active
    if key_request.priority is not None:
        key_info.priority = key_request.priority
    if key_request.status is not None:
        key_info.status = key_request.status
    
    if key_request.quota_limit is not None:
        key_info.quota_limit = key_request.quota_limit
        if key_info.quota_remaining is None:
            key_info.quota_remaining = key_request.quota_limit
    
    keys_db[key_id] = key_info
    
    return key_info

@router.delete("/{key_id}")
async def delete_key(key_id: str):
    """Delete an API key."""
    
    if key_id not in keys_db:
        raise HTTPException(status_code=404, detail=f"Key not found: {key_id}")
    
    del keys_db[key_id]
    
    return {"message": f"Key {key_id} deleted successfully"}
