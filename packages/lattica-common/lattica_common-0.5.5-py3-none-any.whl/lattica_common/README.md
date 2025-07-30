# Lattica Common

A shared utility library for Lattica's homomorphic encryption platform clients.

## Overview

The `lattica_common` package provides core utilities and shared functionality used across Lattica's client libraries. It serves as a foundation for the `lattica_query` and `lattica_management` packages, handling common tasks such as:

1. HTTP communication with Lattica's backend services
2. Authentication and token management
3. File uploads and downloads
4. Version compatibility checks
5. Common utility functions

This package is not typically used directly by end users but is a dependency for Lattica's main client libraries.

## Installation

```bash
pip install lattica-common
```

## Prerequisites

- Python 3.10+
- Requests library

## Key Components

### HTTP Communication

The package provides a robust HTTP client for communicating with Lattica's backend services:

```python
from lattica_common.app_api import HttpClient

# Initialize with your token (optional)
http_client = HttpClient()  # No token for public endpoints
# Or with token for authenticated endpoints
http_client = HttpClient("your_token_here")

# Make API requests
response = http_client.send_http_request("api/endpoint", {"param": "value"})
```

### API Client

The `LatticaAppAPI` class provides a higher-level interface for common API operations and includes a static method for file uploads:

```python
from lattica_common.app_api import LatticaAppAPI

# Initialize with your token
api_client = LatticaAppAPI("your_token_here")

# Upload a file
s3_key = api_client.upload_user_file("path/to/file.pkl")

# Notify server that upload is complete
status = api_client.alert_upload_complete(s3_key)

# Use the static upload method without initializing a client
LatticaAppAPI.upload_file("path/to/file.pkl", "https://upload-url.example.com")
```

### HTTP Settings Management

The package includes utilities for managing HTTP connection settings:

```python
from lattica_common import http_settings

# Configure API endpoints
http_settings.set_be_url("https://api.lattica.ai")
http_settings.set_api_url("https://api.lattica.ai/api/do_action")

# Set global API body parameters
http_settings.set_api_body({"client_id": "my-client"})
```

### Version Management

The package handles client version compatibility with Lattica's backend:

```python
from lattica_common.version_utils import get_module_info

# Get the current module name and version
module_name, module_version = get_module_info()
```

### Development Utilities

Special utilities for development and testing environments:

```python
from lattica_common.dev_utils.dev_mod_utils import RunMode

# Configure to run with local API
from lattica_common.dev_utils.dev_mod_utils import RunMode
from lattica_common import http_settings

# Set to local development mode
RUN_MODE = RunMode.RUN_LOCAL_WITH_API
http_settings.set_be_url("http://localhost:3050")
```

## Exception Handling

The package includes custom exceptions for handling common error scenarios:

```python
from lattica_common.app_api import ClientVersionError

try:
    # Make API request
    response = api_client.some_api_call()
except ClientVersionError as e:
    print(f"Version incompatibility: {e}. Minimum version: {e.min_version}")
```

## Integration with Other Lattica Packages

This package is designed to be used alongside other Lattica client libraries:

```python
# Initialize API clients in other packages
from lattica_query.lattica_query_client import QueryClient
from lattica_management.lattica_management import LatticaManagement

# Both packages utilize lattica_common under the hood
query_client = QueryClient("query_token")
management_client = LatticaManagement("account_token")
```

## Security Considerations

- Handles token-based authentication for secure communication with Lattica's backend
- Manages HTTPS connections for secure data transmission
- Supports version compatibility checks to ensure secure client-server interactions

## License

Proprietary - © Lattica AI

---

For more information, visit [https://www.lattica.ai](https://www.lattica.ai)