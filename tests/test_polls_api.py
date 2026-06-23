import pytest

from conftest import assert_status_code


def _extract_poll_id(response_json):
    return response_json.get("id") or response_json.get("pollId")


def _extract_vote_payload(created_poll, fallback_vote_payload):
    options = created_poll.get("options") or created_poll.get("choices") or []

    if options and isinstance(options[0], dict):
        option_id = options[0].get("id") or options[0].get("optionId") or options[0].get("choiceId")
        if option_id is not None:
            return {"optionId": option_id}

    return fallback_vote_payload


def test_get_all_polls(api_client):
    endpoint = "/api/polls"

    response = api_client.get(endpoint)

    assert_status_code(response, 200, endpoint)
    assert isinstance(response.json(), list)


def test_create_poll(api_client, test_data):
    endpoint = "/api/polls"

    response = api_client.post(endpoint, json=test_data["valid_poll"])

    assert_status_code(response, [200, 201], endpoint)
    body = response.json()
    assert body.get("question") == test_data["valid_poll"]["question"]


def test_get_poll_by_id_after_create(api_client, test_data):
    create_endpoint = "/api/polls"
    create_response = api_client.post(create_endpoint, json=test_data["valid_poll"])
    assert_status_code(create_response, [200, 201], create_endpoint)

    poll_id = _extract_poll_id(create_response.json())
    if poll_id is None:
        pytest.skip("Created poll response does not include a poll ID.")

    get_endpoint = f"/api/polls/{poll_id}"
    get_response = api_client.get(get_endpoint)

    assert_status_code(get_response, 200, get_endpoint)
    assert _extract_poll_id(get_response.json()) == poll_id


def test_vote_for_poll_after_create(api_client, test_data):
    create_endpoint = "/api/polls"
    create_response = api_client.post(create_endpoint, json=test_data["valid_poll"])
    assert_status_code(create_response, [200, 201], create_endpoint)

    created_poll = create_response.json()
    poll_id = _extract_poll_id(created_poll)
    if poll_id is None:
        pytest.skip("Created poll response does not include a poll ID.")

    vote_payload = _extract_vote_payload(created_poll, test_data["valid_vote"])
    vote_endpoint = f"/api/polls/{poll_id}/vote"
    vote_response = api_client.post(vote_endpoint, json=vote_payload)

    assert_status_code(vote_response, [200, 201], vote_endpoint)
