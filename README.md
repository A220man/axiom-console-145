# axiom-console-145

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


AI/ML developer tools platform with 10.1B tokens per month across 87 free LLM providers

## Overview

axiom-console-145 is a self-hosted AI/ML developer tools platform that provides access to 1,313 free model endpoints through a single unified API interface. It includes smart routing, automatic failover, and encrypted key management for personal experimentation with various LLM providers.

## Features

- **Unified API Access**: Single `/v1` endpoint for all LLM providers
- **87 Free LLM Providers**: Access to 1,313 free model endpoints
- **Smart Routing**: Intelligent load balancing across providers
- **Automatic Failover**: Seamless switching between providers on failures
- **Key Management**: Secure storage and management of API keys
- **Health Monitoring**: Real-time provider health status
- **Usage Analytics**: Track usage and performance across all providers
- **Configuration**: Custom endpoints and priority management

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd axiom-console-145

# Install dependencies
pip install -r requirements.txt

# Start the application
python main.py
```

### API Endpoints

- `GET /` - API information
- `GET /v1/health` - Health check
- `GET /v1/health/stats` - Usage statistics
- `GET /v1/models` - List all available models
- `GET /v1/models/providers` - List all providers
- `GET /v1/keys` - List API keys (with filtering)
- `GET /v1/keys/{id}` - Get specific key
- `POST /v1/keys` - Create new API key
- `PUT /v1/keys/{id}` - Update API key
- `DELETE /v1/keys/{id}` - Delete API key

### Key Filtering

When retrieving keys, you can filter by:
- `provider` - Filter by provider name
- `status` - Filter by key status (healthy, issues, disabled)
- `is_active` - Filter by active status

## Models

The API provides access to several popular models:

### OpenAI Models
- `gpt-4` - Advanced reasoning and complex tasks
- `gpt-3.5-turbo` - Fast responses for simpler tasks

### Anthropic Models  
- `claude-3-opus` - Complex reasoning and analysis

### Google Models
- `gemini-pro` - Versatile multimodal capabilities

## Development

This project uses FastAPI for the API server. To run tests:

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/
```

## Configuration

Configuration can be added to `config.json`:
- Provider endpoints
- API key priorities
- Routing preferences
- Health check thresholds

## Running Tests

This project includes comprehensive tests to ensure API functionality:

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only  
pytest tests/integration/
```

## Issues and Features

### Current Issues

1. **Keys page filter tabs**: Selected filter tab label visibility issues in both light and dark themes
2. **Add Key button**: White-on-white text in dark theme makes label unreadable
3. **Header overflow**: Quota Signals button clipped at right edge in dark theme
4. **Custom keys filtering**: All Custom keys listed when filtering for issues, regardless of actual status
5. **App closure**: Unable to close app, right-click tray icon disabled
6. **API additions**: Issues adding certain providers (AI SENSE, HAL-X)

### Planned Features

1. **Latency-Aware Routing**: Real-time connection latency and quota preservation
2. **Webz.io Integration**: News search provider integration
3. **VSCode Agent Feature**: AI-powered software development assistance

## License

MIT License

Maintainer: Ryan Vo <ryandtvo@gmail.com>
