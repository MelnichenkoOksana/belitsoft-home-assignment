import pytest
import requests

SERVICE_UNAVAILABLE_CODES = {502, 503, 504}


def assert_or_xfail_service_unavailable(
    response: requests.Response,
    expected_code: int = 200
) -> None:
    """
    Validates the HTTP response status code with resilience to temporary
    unavailability of httpbin.org.

    If the service returns a known set of transient failure codes (502, 503, 504),
    the test is marked as xfail in order to prevent unstable external infrastructure
    from causing false test failures.

    Args:
        response: The HTTP response object returned by the request.
        expected_code: Expected successful HTTP status code. Defaults to 200.

    Behavior:
        - If status is in SERVICE_UNAVAILABLE_CODES -> pytest.xfail()
        - Otherwise -> assert the status code matches expected_code.
    """

    status = response.status_code

    # If httpbin is temporarily down -> mark the test as expected failure
    if status in SERVICE_UNAVAILABLE_CODES:
        pytest.xfail(
            f"httpbin.org returned transient error {status}. "
            f"Marking test as xfail to avoid false negatives."
        )

    # Otherwise ensure that the response code matches expectation
    assert status == expected_code, (
        f"Expected status {expected_code}, but got {status}"
    )

