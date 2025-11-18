import pytest
import allure
from src.core.httpbin_guard import assert_or_xfail_service_unavailable


@allure.feature("Smoke")
@allure.story("Basic availability check for GET /get")
@pytest.mark.api
@pytest.mark.smoke
def test_smoke_get(http):
    """
    Simple smoke test to check that httpbin GET /get is reachable and
    responds successfully. If the public service is temporarily unavailable
    (after all retries), the test is marked as xfail instead of hard failure.
    """
    with allure.step("Send basic GET /get request"):
        try:
            response = http.request("get", "/get", params={"ping": "pong"})
        except RuntimeError as exc:
            # our retry decorator raises RuntimeError("retryable status 503")
            if "retryable status 503" in str(exc):
                pytest.xfail("httpbin is unavailable after retries (503)")
            raise  # any other RuntimeError is a real failure

    with allure.step("Verify service responded successfully"):
        assert_or_xfail_service_unavailable(response)
        assert response.status_code == 200
