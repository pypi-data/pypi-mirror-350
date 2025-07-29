# aiopythonik

Asynchronous wrapper for the
[pythonik](https://pypi.org/project/nsa-pythonik/) library, enabling its
use in async Python applications without blocking the event loop.

[![PyPI Version](https://img.shields.io/pypi/v/aiopythonik.svg)](https://pypi.org/project/aiopythonik/)
[![Python Versions](https://img.shields.io/pypi/pyversions/aiopythonik.svg)](https://pypi.org/project/aiopythonik/)
[![License](https://img.shields.io/pypi/l/aiopythonik.svg)](https://pypi.org/project/aiopythonik/)

## Overview

`aiopythonik` provides asynchronous versions of pythonik functionality
by wrapping the synchronous operations in a thread pool executor. This
approach is similar to how `aioboto3` wraps `boto3`, allowing you to use
asynchronous syntax while maintaining the original library's
capabilities.

### Features

- Complete async API for the pythonik library
- Automatic thread pool management for non-blocking operations
- Built-in rate limit handling with configurable retry strategies
- Extended functionality through patched pythonik methods
- Support for Python 3.11+

## Installation

### Requirements

- Python 3.11 or higher

```bash
# Install from PyPI (recommended for most users)
pip install aiopythonik
```

The required dependency `nsa-pythonik` will be automatically installed.

### Installing from Source

For development or to get the latest unreleased changes:

```bash
# Clone the repository
git clone https://bitbucket.org/chesa/aiopythonik.git
cd aiopythonik

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quickstart

```python
import asyncio
from aiopythonik import AsyncPythonikClient

async def main():
    # Initialize the client
    client = AsyncPythonikClient(
        app_id="your_app_id",
        auth_token="your_auth_token",
        timeout=60,
        base_url="https://app.iconik.io",
    )

    try:
        # Use async methods
        asset = await client.assets().get("asset_id")
        print(f"Asset title: {asset.data.title}")

        # Get files for the asset
        files = await client.files().get_asset_files("asset_id")
        print(f"Number of files: {len(files.data.files)}")

        # Search for assets
        from pythonik.models.search.search_body import SearchBody
        search_results = await client.search().search(
            SearchBody(doc_types=["assets"], query="title:sample")
        )
        print(f"Found {len(search_results.data.objects)} assets")

    finally:
        # Always close the client when done
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Using the Context Manager

For convenience, you can use the async context manager to ensure proper
cleanup:

```python
import asyncio
from aiopythonik import AsyncPythonikClientContext

async def main():
    async with AsyncPythonikClientContext(
        app_id="your_app_id",
        auth_token="your_auth_token",
        timeout=60,
        base_url="https://app.iconik.io",
    ) as client:
        # Use async methods
        asset = await client.assets().get("asset_id")
        print(f"Asset title: {asset.data.title}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Coverage

`aiopythonik` provides async wrappers for all pythonik APIs and extends
functionality with some additional methods. Each API from the original
library is accessible through the corresponding async wrapper:

```python
# Assets
asset = await client.assets().get("asset_id")
assets = await client.assets().fetch(params={"per_page": 50})  # Enhanced method
await client.assets().delete("asset_id")

# Collections
collection = await client.collections().get("collection_id")
info = await client.collections().get_info("collection_id")
contents = await client.collections().get_contents("collection_id")

# Files
files = await client.files().get_asset_files("asset_id")
# Enhanced method with automatic checksum calculation
files_by_checksum = await client.files().get_files_by_checksum("d41d8cd98f00b204e9800998ecf8427e")
# Or calculate checksum automatically from a file
files_by_file = await client.files().get_files_by_checksum("path/to/file.mp4")

# Metadata
views = await client.metadata().get_views()
view = await client.metadata().get_view("view_id")
metadata = await client.metadata().get_asset_metadata("asset_id", "view_id")

# Jobs
job = await client.jobs().get("job_id")
await client.jobs().cancel("job_id")
```

### Automatic Rate Limit Handling

The library includes built-in handling for API rate limits:

```python
from aiopythonik import AsyncPythonikClient, RateLimitConfig

# Configure custom rate limiting behavior
rate_limit_config = RateLimitConfig(
    max_retries=5,              # Maximum number of retries for rate-limited requests
    initial_backoff=1.0,        # Initial backoff in seconds
    max_backoff=30.0,           # Maximum backoff in seconds
    backoff_factor=2.0,         # Exponential backoff factor
    jitter=True                 # Add randomness to backoff times
)

client = AsyncPythonikClient(
    app_id="your_app_id",
    auth_token="your_auth_token",
    rate_limit_config=rate_limit_config
)

# Rate-limited requests will automatically be retried with backoff
```

## Advanced Usage

### Concurrent Operations

Running multiple operations concurrently:

```python
import asyncio
from aiopythonik import AsyncPythonikClientContext

async def main():
    async with AsyncPythonikClientContext(
        app_id="your_app_id",
        auth_token="your_auth_token",
    ) as client:
        # Run multiple operations concurrently
        asset_ids = ["id1", "id2", "id3", "id4", "id5"]

        tasks = [client.assets().get(asset_id) for asset_id in asset_ids]
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results):
            print(f"Asset {i+1}: {result.data.title}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Base URL

If you need to use a different API endpoint:

```python
client = AsyncPythonikClient(
    app_id="your_app_id",
    auth_token="your_auth_token",
    base_url="https://custom.iconik.io"
)
```

### Customizing Thread Pool Size

Control the maximum number of worker threads:

```python
client = AsyncPythonikClient(
    app_id="your_app_id",
    auth_token="your_auth_token",
    max_workers=10  # Set maximum number of worker threads
)
```

## Rate Limiting Details

The iconik APIs implement rate limiting to prevent individual users from
negatively impacting system performance. By default, the `aiopythonik`
library includes automatic handling of rate limits using a retry
strategy with exponential backoff.

Rate limits are enforced per authenticated user and application token:

- 50 requests per second sustained
- 1000 requests over any 20 second period

When a rate limit is reached, the API responds with
`429 Too Many Requests`. The library will automatically retry these
requests after an appropriate delay according to the configured retry
strategy.

You can also disable automatic retry handling if you prefer to manage
rate limiting yourself:

```python
client = AsyncPythonikClient(
    app_id="your_app_id",
    auth_token="your_auth_token",
    disable_rate_limit_handling=True
)
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
