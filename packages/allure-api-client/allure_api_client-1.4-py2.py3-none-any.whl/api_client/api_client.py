from __future__ import annotations

from http import HTTPStatus
from typing import Any
from typing import Callable

from httpx import Client
from httpx import Cookies
from pydantic import HttpUrl

from api_client.hooks import allure_request_hook
from api_client.hooks import allure_response_hook
from api_client.hooks import request_hook
from api_client.hooks import response_hook
from api_client.status_code_method import check_status_code


class APIClient(Client):
    """
    This class extends the httpx.Client class to provide an easy way to make HTTP requests to a specific API.
    It includes functionality to set base URL, authentication, cookies, and SSL verification for all requests made through it.

    Attributes:
        auth (Callable[..., Any] | object, optional): An authentication object or callable to be used for request authorization.
        cookies (Cookies | None, optional): Cookies to be sent with each request. Defaults to None.
        base_url (HttpUrl): The base URL to which the API endpoints will be appended for all requests.

    Args:
        base_url (HttpUrl): The base URL to be used for requests.
        cookies (Cookies | None, optional): Cookies to be used with requests. If None, no cookies will be sent.
        auth (Callable[..., Any] | object | None, optional): An authentication object or callable for request authorization.
            If None, no authentication will be used. Defaults to None.
        verify (bool, optional): Determines whether to verify SSL certificates for HTTPS requests. Defaults to False.
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

    def send_request(
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
    ):
        """
        Sends an HTTP request using the specified method to a path appended to the base URL.

        Args:
            method (str): The HTTP method to use (e.g., 'GET', 'POST').
            path (str): The API endpoint path to be appended to the base URL.
            headers (dict | None, optional): Headers to send with the request. Defaults to None.
            params (dict | None, optional): Query parameters to append to the URL. Defaults to None.
            data (dict | None, optional): Data to send in the body of the request. Defaults to None.
            json (dict | None, optional): JSON data to send in the body of the request. Defaults to None.
            files (dict | list | None, optional): Files to send in the request. Defaults to None.
            follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.
            timeout (int, optional): The number of seconds to wait for the server to send data before giving up. Defaults to 300.
            status_code (int, optional): The expected HTTP status code for a successful request. Defaults to HTTPStatus.OK.

        Returns:
            Response: The HTTP response object.

        Raises:
            HTTPStatusError: If the response's status code does not match the expected status code.

        Example:
        # Example of using the send_request method to perform a GET request
        client = APIClient(base_url="https://api.example.com")
        response = client.send_request(
            method="GET",
            path="/users",
            params={"page": 2},
            headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
        )
        print(response.json())

        # This will send a request to "https://api.example.com/users?page=2"
        # with the specified authorization header and return the JSON response.
        """
        response = self.request(
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
