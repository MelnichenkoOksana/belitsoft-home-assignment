import json
import uuid

import pytest
import allure

from src.core.httpbin_guard import assert_or_xfail_service_unavailable


@allure.feature("Request inspection")
@allure.story("GET /get echoes query params")
@pytest.mark.api
def test_get_echoes_query_params(http, random_query):
    """
    Verify that GET /get echoes back provided query parameters.
    """
    with allure.step("Send GET /get with random query params"):
        response = http.request("get", "/get", params=random_query)
        assert_or_xfail_service_unavailable(response)

    with allure.step("Verify echoed query params match the request"):
        body = response.json()
        allure.attach(
            json.dumps(body, indent=2),
            name="GET /get body",
            attachment_type=allure.attachment_type.JSON,
        )
        assert body["args"] == random_query


@allure.feature("Request inspection")
@allure.story("POST /post echoes JSON body")
@pytest.mark.api
def test_post_json_echoes_body(http, user_payload):
    """
    Verify that POST /post echoes JSON payload in the 'json' field of the response.
    """
    payload = user_payload.to_dict()

    with allure.step("Send POST /post with JSON payload"):
        response = http.request("post", "/post", json=payload)
        assert_or_xfail_service_unavailable(response)

    with allure.step("Verify echoed JSON body matches the request payload"):
        body = response.json()
        allure.attach(
            json.dumps(body, indent=2),
            name="POST /post body",
            attachment_type=allure.attachment_type.JSON,
        )
        assert body["json"] == payload


@allure.feature("Response formats")
@allure.story("JSON response")
@pytest.mark.api
def test_response_format_json(http):
    """
    Verify that GET /json returns a valid JSON document with JSON content type.
    Additionally assert that the current httpbin implementation returns a
    'slideshow' root field.
    """
    with allure.step("Send GET /json"):
        response = http.request("get", "/json")
        assert_or_xfail_service_unavailable(response)

    with allure.step("Verify status code is 200"):
        allure.attach(
            str(response.status_code),
            name="status_code",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert response.status_code == 200

    with allure.step("Verify Content-Type is 'application/json'"):
        content_type = response.headers.get("Content-Type", "")
        allure.attach(
            content_type,
            name="Content-Type",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert "application/json" in content_type

    with allure.step("Verify body is a JSON object and contains 'slideshow' field"):
        body = response.json()
        allure.attach(
            json.dumps(body, indent=2),
            name="JSON body",
            attachment_type=allure.attachment_type.JSON,
        )
        assert isinstance(body, dict)
        assert "slideshow" in body


@allure.feature("Response formats")
@allure.story("HTML response")
@pytest.mark.api
def test_response_format_html(http):
    """
    Verify that GET /html returns HTML content with 'text/html' content type.
    """
    with allure.step("Send GET /html"):
        response = http.request("get", "/html")
        assert_or_xfail_service_unavailable(response)

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify Content-Type is 'text/html'"):
        content_type = response.headers.get("Content-Type", "")
        allure.attach(
            content_type,
            name="Content-Type",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert "text/html" in content_type

    with allure.step("Verify body contains HTML markup"):
        allure.attach(
            response.text,
            name="HTML body",
            attachment_type=allure.attachment_type.HTML,
        )
        assert "<html" in response.text.lower()


import allure
import pytest
from src.core.httpbin_guard import assert_or_xfail_service_unavailable


@allure.feature("Request inspection")
@allure.story("GET /headers echoes back custom headers")
@pytest.mark.api
def test_request_inspection_headers(http):
    """Verify that GET /headers returns sent custom headers."""

    custom_header = {"X-Test-Header": "aqa-home-assignment"}

    with allure.step("Send GET /headers with custom header"):
        allure.attach(
            str(custom_header),
            name="Sent headers",
            attachment_type=allure.attachment_type.TEXT,
        )
        response = http.request("get", "/headers", headers=custom_header)
        assert_or_xfail_service_unavailable(response)

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify custom header is present in response"):
        body = response.json()
        echoed_value = body["headers"].get("X-Test-Header")
        allure.attach(
            str(body),
            name="Response JSON",
            attachment_type=allure.attachment_type.JSON,
        )
        assert echoed_value == "aqa-home-assignment"



@allure.feature("Request inspection")
@allure.story("User-Agent header")
@pytest.mark.api
def test_request_inspection_user_agent(http):
    """
    Verify that GET /user-agent returns the User-Agent sent in the request.
    """
    user_agent = "aqa-httpbin-tests/1.0"

    with allure.step("Send GET /user-agent with custom User-Agent"):
        response = http.request("get", "/user-agent", headers={"User-Agent": user_agent})
        assert_or_xfail_service_unavailable(response)

    with allure.step("Verify User-Agent is echoed back in the response"):
        body = response.json()
        allure.attach(
            json.dumps(body, indent=2),
            name="GET /user-agent body",
            attachment_type=allure.attachment_type.JSON,
        )
        assert body["user-agent"] == user_agent


@allure.feature("Dynamic data")
@allure.story("UUID generation")
@pytest.mark.api
def test_dynamic_uuid(http):
    """
    Verify that GET /uuid returns valid UUID4 values and that two consecutive
    calls return different values (dynamic data).
    """
    with allure.step("Send two GET /uuid requests"):
        response_1 = http.request("get", "/uuid")
        response_2 = http.request("get", "/uuid")

        assert_or_xfail_service_unavailable(response_1)
        assert_or_xfail_service_unavailable(response_2)

    with allure.step("Extract UUIDs from both responses"):
        uuid_1 = response_1.json()["uuid"]
        uuid_2 = response_2.json()["uuid"]

        allure.attach(
            json.dumps({"uuid_1": uuid_1, "uuid_2": uuid_2}, indent=2),
            name="UUIDs returned by /uuid",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Verify both UUIDs are valid UUID4"):
        parsed_1 = uuid.UUID(uuid_1)
        parsed_2 = uuid.UUID(uuid_2)

        assert parsed_1.version == 4, f"Expected UUID4, got version {parsed_1.version}"
        assert parsed_2.version == 4, f"Expected UUID4, got version {parsed_2.version}"

    with allure.step("Verify UUIDs are different (dynamic data)"):
        assert uuid_1 != uuid_2
