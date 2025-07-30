from __future__ import annotations

from http import HTTPStatus
from typing import Any
from typing import Callable

from httpx import AsyncClient
from httpx import Cookies
from httpx import Response
from pydantic import HttpUrl

from api_client.hooks import allure_request_hook
from api_client.hooks import allure_response_hook
from api_client.hooks import request_hook
from api_client.hooks import response_hook
from api_client.status_code_method import check_status_code


class AsyncAPIClient(AsyncClient):
    """
    A subclass of httpx.AsyncClient, AsyncAPIClient provides a convenient interface for asynchronous HTTP requests
    to a specified base URL. It integrates additional features like automatic bearer token authentication, cookie management,
    SSL certificate verification control, and hooks for request and response logging. Ideal for use in asynchronous environments
    or frameworks.

    Attributes:
        auth (Callable[..., Any] | object, optional): Authentication handler for requests, supporting callable or object formats.
        cookies (Cookies | None, optional): Cookie storage for managing cookies across multiple requests.
        base_url (HttpUrl): The root URL to which endpoint paths will be appended for requests.

    Args:
        base_url (HttpUrl): The root URL for all API requests.
        cookies (Cookies | None, optional): Initial cookie store for the client.
        auth (Callable[..., Any] | object | None, optional): Authentication handler to be used for all requests.
        verify (bool, optional): Flag to enable or disable SSL certificate verification. Defaults to False for flexibility in testing environments.

    Example:
        async with AsyncAPIClient(base_url="https://api.example.com", verify=True) as client:
            response = await client.send_request("GET", "/data")
            print(response.json())
    """

    def __init__(
            self,
            base_url: HttpUrl | str,
            cookies: Cookies | None = None,
            auth: Callable[..., Any] | object | None = None,
            verify: bool = False,
            with_allure: bool = True,
    ) -> None:
        if with_allure:
            super().__init__(auth=None, verify=verify, event_hooks={'request': [allure_request_hook],
                                                                    'response': [allure_response_hook]})
        else:
            super().__init__(auth=None, verify=verify, event_hooks={'request': [request_hook],
                                                                    'response': [response_hook]})
        self.auth = auth
        self.cookies = cookies
        self.base_url = base_url

    async def send_request(
            self,
            method: str,
            path: str,
            headers: dict | None = None,
            params: dict | None = None,
            data: dict | None = None,
            json: dict | None = None,
            files: dict | list | None = None,
            follow_redirects: bool = True,
            timeout=300,
            status_code: int = HTTPStatus.OK,
    ) -> Response:
        """
        Asynchronously sends an HTTP request using the specified method and path.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            path (str): API endpoint path to append to the base URL.
            headers (dict | None, optional): Headers to include in the request.
            params (dict | None, optional): URL parameters to include in the request.
            data (dict | None, optional): Form data to include in the request body.
            json (dict | None, optional): JSON data to include in the request body.
            files (dict | list | None, optional): Files to include in the request.
            follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.
            timeout (int, optional): Request timeout in seconds. Defaults to 300.
            status_code (int, optional): Expected HTTP status code for successful requests. Defaults to HTTPStatus.OK.

        Returns:
            Response: The httpx.Response object from the asynchronous request.

        Raises:
            HTTPStatusError: If the response's status code does not match the expected status code.

        Example:
            async with AsyncAPIClient(base_url="https://api.example.com") as client:
                response = await client.send_request(
                    "GET",
                    "/resource",
                    headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
                )
                data = response.json()
                print(data)
        """
        response = await self.request(
            method=method,
            url=f'{self.base_url}{path}',
            headers=headers, params=params,
            data=data, json=json,
            files=files, auth=self.auth, cookies=self.cookies,
            follow_redirects=follow_redirects,
            timeout=timeout,
        )
        check_status_code(response=response, status_code=status_code)
        return response
