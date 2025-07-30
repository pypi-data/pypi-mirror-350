from httpx import Response


def check_status_code(response: Response, status_code: int) -> None:
    """
    Verifies if the HTTP response status code matches the expected status code.

    This function is designed to be used in testing scenarios to assert that the HTTP response received has the correct
    status code. If the response status code does not match the expected status code, an AssertionError is raised with a
    detailed message. The check and its result are recorded as a step in the Allure test report for traceability and
    easier debugging.

    Args:
        response: The httpx.Response object to be checked.
        status_code (int): The expected HTTP status code to validate against the response's status code.

    Raises:
        AssertionError: If the response's status code does not match the expected status code. The error message includes
        the expected code, the received code, and the response body.

    Example:
        # Assuming 'client' is an instance of httpx.Client
        response = client.get('https://example.com/api/resource')
        check_status_code(response, 200) # Checks if the status code of the response is 200
    """
    assert response.status_code == status_code, \
        f"""Wrong status code, expected: {status_code}, received: {response.status_code}
            message: {response.text}"""
