# API package for axiom-console-145 AI/ML developer tools platform

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .routes.v1 import router as v1_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="axiom-console-145 API",
        description="AI/ML developer tools platform with 10.1B tokens per month across 87 free LLM providers",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # CORS middleware for cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    
    # Include V1 API routes
    app.include_router(v1_router, prefix="/v1")
    
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "axiom-console-145 API",
            "description": "AI/ML developer tools platform with 10.1B tokens per month across 87 free LLM providers",
            "version": "0.1.0",
            "endpoints": [
                "/v1/models",
                "/v1/providers", 
                "/v1/keys",
                "/v1/health"
            ]
        }
    
    @app.get("/health")
    async def health_check():
        """Basic health check endpoint."""
        return {
            "status": "healthy",
            "timestamp": "2026-11-13T08:25:03Z",
            "version": "0.1.0"
        }
    
    return app
