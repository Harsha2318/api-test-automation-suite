import json
from pathlib import Path

import pytest
from dotenv import load_dotenv

from utils.api_client import APIClient, get_base_url


load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    return get_base_url()


@pytest.fixture(scope="session")
def api_client(base_url: str) -> APIClient:
    return APIClient(base_url=base_url)


@pytest.fixture(scope="session")
def test_data() -> dict:
    data_file = Path(__file__).parent / "config" / "test_data.json"
    with data_file.open(encoding="utf-8") as file:
        return json.load(file)


def print_response_details(endpoint: str, response) -> None:
    print(f"\nEndpoint: {endpoint}")
    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")


def assert_status_code(response, expected_status_codes, endpoint: str) -> None:
    if isinstance(expected_status_codes, int):
        expected_status_codes = [expected_status_codes]

    print_response_details(endpoint, response)

    assert response.status_code in expected_status_codes, (
        f"Expected status code {expected_status_codes} for {endpoint}, "
        f"but got {response.status_code}. Response: {response.text}"
    )
