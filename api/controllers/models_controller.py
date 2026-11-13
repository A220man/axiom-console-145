from fastapi import HTTPException, APIRouter
from api.models import ModelInfo, ProviderInfo

# Create router
router = APIRouter()


@router.get("/", response_model=list[ModelInfo])
async def get_models():
    """Get all available models."""
    
    models = [
        ModelInfo(
            id="gpt-4",
            created=1691961600,
            owned_by="openai",
            description="GPT-4 model for advanced tasks",
            max_tokens=8192,
            context_window=8192,
            pricing={"input": 0.03, "output": 0.06},
            capabilities={"text_completion": True, "chat": True}
        ),
        ModelInfo(
            id="gpt-3.5-turbo",
            created=1691961500,
            owned_by="openai", 
            description="GPT-3.5 Turbo for faster responses",
            max_tokens=4096,
            context_window=16385,
            pricing={"input": 0.0015, "output": 0.002},
            capabilities={"text_completion": True, "chat": True}
        ),
        ModelInfo(
            id="claude-3-opus",
            created=1691961400,
            owned_by="anthropic",
            description="Claude 3 Opus for complex reasoning",
            max_tokens=4096,
            context_window=200000,
            pricing={"input": 0.015, "output": 0.075},
            capabilities={"text_completion": True, "chat": True, "analysis": True}
        ),
        ModelInfo(
            id="gemini-pro",
            created=1691961300,
            owned_by="google",
            description="Google Gemini Pro model",
            max_tokens=2048,
            context_window=32768,
            pricing={"input": 0.001, "output": 0.002},
            capabilities={"text_completion": True, "chat": True}
        )
    ]
    
    return models


@router.get("/providers", response_model=list[ProviderInfo])
async def get_providers():
    """Get all available providers."""
    
    providers = [
        ProviderInfo(
            id="openai",
            name="OpenAI",
            description="OpenAI's API for various models including GPT-4, GPT-3.5, and DALL-E",
            models_available=50,
            is_active=True,
            health_status="healthy",
            endpoint="https://api.openai.com/v1",
            capabilities={"chat": True, "text_completion": True, "image": True}
        ),
        ProviderInfo(
            id="anthropic",
            name="Anthropic",
            description="Anthropic's API for Claude models",
            models_available=15,
            is_active=True,
            health_status="healthy",
            endpoint="https://api.anthropic.com/v1",
            capabilities={"chat": True, "analysis": True}
        ),
        ProviderInfo(
            id="google",
            name="Google AI",
            description="Google's AI platform including Gemini models",
            models_available=25,
            is_active=True,
            health_status="degraded",
            endpoint="https://generativelanguage.googleapis.com/v1",
            capabilities={"chat": True, "text_completion": True}
        ),
        ProviderInfo(
            id="custom",
            name="Custom OpenAI-Compatible",
            description="Custom endpoints compatible with OpenAI API",
            models_available=313,
            is_active=True,
            health_status="healthy",
            endpoint="custom://user-provided",
            capabilities={"chat": True, "text_completion": True}
        )
    ]
    
    return providers
