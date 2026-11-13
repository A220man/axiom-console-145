#!/usr/bin/env python3
"""
Main entry point for axiom-console-145 AI/ML developer tools platform.

This FastAPI application provides a unified interface to 1,313+ free LLM model endpoints
across 87 providers with smart routing and automatic failover capabilities.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from api import create_app
import uvicorn


def main():
    """Run the axiom-console-145 API server."""
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    # Create the FastAPI application
    app = create_app()
    
    # Run the server
    print(f"Starting axiom-console-145 API server on {host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"Health Check: http://{host}:{port}/health")
    print(f"API Version: 0.1.0")
    print(f"Total Providers: 87")
    print(f"Available Models: 1,313+")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        debug=debug,
        reload=debug,
        access_log=True
    )


if __name__ == "__main__":
    main()
