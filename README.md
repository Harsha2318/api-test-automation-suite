# API Test Automation Suite

A Python-based REST API automation suite for testing a Spring Boot Polling Application backend.

The project uses `pytest` and the `requests` library to validate API health, poll creation, poll retrieval, voting, and negative request scenarios. It also generates an HTML report and includes a Jenkins pipeline for CI execution.

## Features

```text
Environment-based API testing using BASE_URL
Reusable API client wrapper
Positive and negative REST API test cases
JSON-based test data
HTML test report generation
Jenkins pipeline support
Readable failure logs with endpoint, status code, and response body
```

## Tech Stack

```text
Python
Pytest
Requests
pytest-html
python-dotenv
Jenkins
```

## Target API

The test suite is designed for a Spring Boot Polling Application with endpoints similar to:

```text
GET  /actuator/health
GET  /api/polls
POST /api/polls
GET  /api/polls/{id}
POST /api/polls/{id}/vote
```

Default backend URL:

```text
http://localhost:8080
```

## Folder Structure

```text
api-test-automation-suite/
|
|-- config/
|   `-- test_data.json
|
|-- reports/
|   `-- .gitkeep
|
|-- tests/
|   |-- test_health.py
|   |-- test_negative_cases.py
|   `-- test_polls_api.py
|
|-- utils/
|   `-- api_client.py
|
|-- .gitignore
|-- conftest.py
|-- Jenkinsfile
|-- pytest.ini
|-- README.md
`-- requirements.txt
```

## Test Coverage

Positive test cases:

```text
Backend health check
Get all polls
Create a poll
Get poll by ID after creating a poll
Vote for a poll after creating a poll
```

Negative test cases:

```text
Get poll using invalid poll ID
Create poll with empty payload
Create poll with empty question
Create poll with missing options
Vote using invalid poll ID
```

## Prerequisites

Install Python 3.10 or higher.

Make sure the Spring Boot backend is running before executing the tests.

Check Python version:

```bash
python --version
```

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Activate the virtual environment on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

Run all tests using the default API URL:

```bash
pytest
```

Run tests with a custom API URL on Windows PowerShell:

```powershell
$env:BASE_URL="http://localhost:8080"
pytest
```

Run tests with a custom API URL on Command Prompt:

```bat
set BASE_URL=http://localhost:8080
pytest
```

Run tests with a custom API URL on Linux/macOS:

```bash
BASE_URL=http://localhost:8080 pytest
```

## Running Specific Tests

Run health check tests:

```bash
pytest tests/test_health.py
```

Run poll API tests:

```bash
pytest tests/test_polls_api.py
```

Run negative test cases:

```bash
pytest tests/test_negative_cases.py
```

Run tests with verbose output:

```bash
pytest -v
```

## HTML Report

The project uses `pytest-html` to generate a report automatically.

Report location:

```text
reports/api_test_report.html
```

Manual report command:

```bash
pytest --html=reports/api_test_report.html --self-contained-html
```

Open the generated HTML file in a browser to view test results.

## Configuration

The base API URL is read from the `BASE_URL` environment variable.

If `BASE_URL` is not provided, the test suite uses:

```text
http://localhost:8080
```

Test data is stored in:

```text
config/test_data.json
```

Pytest settings are stored in:

```text
pytest.ini
```

## Jenkins Pipeline

The included `Jenkinsfile` runs the API tests in a CI pipeline.

Pipeline stages:

```text
Checkout Code
Set Up Python Virtual Environment
Install Dependencies
Run Pytest API Tests and Generate HTML Report
Publish HTML Report
```

The Jenkins pipeline accepts a `BASE_URL` parameter. Set it to the backend URL you want to test:

```text
http://localhost:8080
```

Required Jenkins plugin:

```text
HTML Publisher Plugin
```

After execution, Jenkins publishes the HTML report as:

```text
API Test Automation Report
```

## Debugging

When a test fails, the test output includes:

```text
Endpoint
Status code
Response body
```

This makes it easier to identify backend response issues, invalid payloads, or environment configuration problems.

## Notes

The tests assume that the backend API follows the expected endpoint structure and returns JSON responses.

If your backend uses different field names for poll IDs or vote options, update the helper functions in:

```text
tests/test_polls_api.py
```

## Future Enhancements

```text
Add JSON schema validation
Add Docker support for test execution
Add GitHub Actions workflow
Add Allure reporting
Add more test data files for different API scenarios
```
