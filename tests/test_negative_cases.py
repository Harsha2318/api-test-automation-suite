from conftest import assert_status_code


def test_get_poll_with_invalid_id(api_client, test_data):
    invalid_poll_id = test_data["invalid_poll_id"]
    endpoint = f"/api/polls/{invalid_poll_id}"

    response = api_client.get(endpoint)

    assert_status_code(response, [400, 404], endpoint)


def test_create_poll_with_empty_payload(api_client, test_data):
    endpoint = "/api/polls"

    response = api_client.post(endpoint, json=test_data["empty_payload"])

    assert_status_code(response, [400, 422], endpoint)


def test_create_poll_with_empty_question(api_client, test_data):
    endpoint = "/api/polls"

    response = api_client.post(endpoint, json=test_data["invalid_poll_empty_question"])

    assert_status_code(response, [400, 422], endpoint)


def test_create_poll_with_missing_options(api_client, test_data):
    endpoint = "/api/polls"

    response = api_client.post(endpoint, json=test_data["invalid_poll_missing_options"])

    assert_status_code(response, [400, 422], endpoint)


def test_vote_with_invalid_poll_id(api_client, test_data):
    invalid_poll_id = test_data["invalid_poll_id"]
    endpoint = f"/api/polls/{invalid_poll_id}/vote"

    response = api_client.post(endpoint, json=test_data["invalid_vote"])

    assert_status_code(response, [400, 404, 422], endpoint)
