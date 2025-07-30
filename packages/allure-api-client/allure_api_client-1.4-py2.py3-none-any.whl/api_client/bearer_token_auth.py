from typing import Generator

from httpx import Auth
from httpx import Request
from httpx import Response


class BearerToken(Auth):
    """
    Custom authentication class that implements bearer token authentication for HTTP requests.

    This class extends the Auth base class from httpx and is used to inject the 'Authorization' header with a bearer token
    into outgoing HTTP requests. It should be passed to the 'auth' parameter of an httpx.Client or any request method.
    The token must be provided at the time of the class instance creation, and it raises an exception if no token is provided.

    Args:
        token (str): The bearer token to be used for authentication.

    Raises:
        Exception: If the token is not provided (i.e., is empty or None).

    Usage Example:
        # Usage with httpx.Client
        token = 'your_bearer_token_here'
        auth = BearerToken(token)
        client = httpx.Client(auth=auth)

        # Making a request with the client will automatically include the bearer token in the header
        response = client.get('https://api.example.com/protected/resource')

    Note:
        The token should be kept secure and should not be hard-coded or exposed in source code for security reasons.
    """

    def __init__(self, token: str) -> None:
        self.token = token
        if not self.token:
            raise Exception("The token is mandatory")

    def auth_flow(
            self, request: Request
    ) -> Generator[Request, Response, None]:
        request.headers['Authorization'] = f'Bearer {self.token}'
        yield request
