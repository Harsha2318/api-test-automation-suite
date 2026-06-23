from conftest import assert_status_code


def test_backend_health_check(api_client):
    endpoint = "/actuator/health"

    response = api_client.get(endpoint)

    assert_status_code(response, 200, endpoint)
    body = response.json()
    assert body.get("status") in ["UP", "DOWN", "UNKNOWN"]
