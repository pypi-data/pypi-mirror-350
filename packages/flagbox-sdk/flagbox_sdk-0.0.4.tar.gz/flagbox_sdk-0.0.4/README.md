# FlagBox Python SDK

A lightweight Python SDK for managing feature flags with FlagBox. This SDK provides both synchronous and asynchronous methods for evaluating feature flags, with support for global and per-flag contexts.

## Installation

```bash
pip install flagbox-sdk
```

## Quick Start

```python
from flagbox import FlagBoxClient

# Initialize the client
client = FlagBoxClient(
    api_url="https://api.flagbox.io",
    api_key="your-api-key"
)

# Get a feature flag value
is_new_feature_enabled = client.get_flag("new-feature", False)

if is_new_feature_enabled:
    # Feature is enabled
    pass
else:
    # Feature is disabled
    pass
```

## Using Context

The SDK supports both global context (set during client initialization) and per-flag context:

```python
# Initialize client with global context
client = FlagBoxClient(
    api_url="https://api.flagbox.io",
    api_key="your-api-key",
    global_context={
        "userId": "user123",
        "plan": "premium"
    }
)

# Get flag with additional per-flag context
result = client.get_flag(
    flag_key="new-feature",
    default_value=False,
    context={
        "country": "Spain"
    }
)
```

## Async Support

For asynchronous applications, use the async version of the client:

```python
import asyncio
from flagbox import FlagBoxClient

async def main():
    client = FlagBoxClient(
        api_url="https://api.flagbox.io",
        api_key="your-api-key"
    )

    # Get a feature flag value asynchronously
    is_new_feature_enabled = await client.get_flag_async(
        "new-feature",
        False
    )

asyncio.run(main())
```

## Error Handling

The SDK handles errors gracefully by returning the default value in case of:

- Network errors
- Invalid API responses
- Unsupported flag types
- Missing flags
- Rate limit exceeded

## Requirements

- Python 3.7 or higher
- requests>=2.25.0
- aiohttp>=3.8.0

## License

MIT
