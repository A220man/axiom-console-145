from fastapi import HTTPException, APIRouter
from datetime import datetime
import random

# Create router
router = APIRouter()


@router.get("/")
async def get_health_check():
    """Get health check information."""
    
    providers_status = {}
    total_providers = 87
    active_providers = 85
    
    # Simulate random provider health
    providers = [f"provider-{i}" for i in range(total_providers)]
    for provider in providers[:10]:  # Check a subset
        providers_status[provider] = random.choice(["healthy", "degraded", "down"])
    
    return {
        "status": "healthy" if active_providers > 0 else "degraded",
        "timestamp": datetime.now().isoformat() + "Z",
        "version": "0.1.0",
        "providers_status": providers_status,
        "total_providers": total_providers,
        "active_providers": active_providers
    }


@router.get("/stats")
async def get_stats():
    """Get usage statistics."""
    
    return {
        "total_requests": 10000,
        "successful_requests": 9850,
        "failed_requests": 150,
        "providers_used": {
            "openai": 4500,
            "anthropic": 2800,
            "google": 1500,
            "custom": 1000,
            "other": 200
        }
    }
