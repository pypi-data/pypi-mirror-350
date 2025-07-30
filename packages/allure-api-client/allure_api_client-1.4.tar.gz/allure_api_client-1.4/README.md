# allure-api-client

The `allure-api-client` library is a Python package designed to facilitate API testing and reporting in Allure. Built on
top of the `httpx` library, it provides both synchronous and asynchronous clients for making HTTP requests, complete
with automatic request and response logging for Allure reports. The library also includes utilities for bearer token
authentication and status code verification.

## Features

- Synchronous and Asynchronous API Clients
- Automatic logging of requests and responses in Allure reports
- Bearer Token Authentication
- Status Code Verification

## Installation

To install `allure-api-client`, you will need Python installed on your system. You can install the library using pip:

```bash
pip install allure-api-client
```

## Usage

### Synchronous API Client

```python
from api_client import APIClient

# Initialize the client
client = APIClient(
    base_url="https://api.example.com",
    auth=BearerToken("YOUR_ACCESS_TOKEN"),  # Optional
    verify=False  # Optional
)

# Send a request
response = client.send_request(
    method="GET",
    path="/endpoint"
)
```

### Asynchronous API Client

```python
from api_client import AsyncAPIClient

# Initialize the client
async with AsyncAPIClient(
        base_url="https://api.example.com",
        auth=BearerToken("YOUR_ACCESS_TOKEN"),  # Optional
        verify=False  # Optional
) as client:
    # Send a request
    response = await client.send_request(
        method="GET",
        path="/endpoint"
    )
```

### Bearer Token Authentication

```python
from api_client import BearerToken

# Initialize the bearer token
auth = BearerToken("YOUR_ACCESS_TOKEN")

# Use the auth with APIClient or AsyncAPIClient
```

### Checking Status Code

```python
from api_client import check_status_code

# After receiving a response
check_status_code(response, 200)  # Verifies that the status code is 200
```

## Contributing

Contributions to `allure-api-client` are welcome! Please follow the standard procedures to submit issues, pull requests,
etc.

## License

`allure-api-client` is released under the [MIT License](LICENSE).
