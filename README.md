# API Test Automation Suite

Python-based REST API test automation project for validating a Spring Boot Polling Application backend.

This project is designed to be simple, practical, and resume-friendly for QA automation, DevOps, backend testing, and graduate trainee roles.

## Project Overview

The suite validates common REST API workflows using Pytest and the Requests library. It supports environment-based execution through `BASE_URL`, generates HTML reports using `pytest-html`, and includes a Jenkins pipeline for CI/CD validation.

Target API endpoints:

```text
GET  /actuator/health
GET  /api/polls
POST /api/polls
GET  /api/polls/{id}
POST /api/polls/{id}/vote
```

## Tech Stack

```text
Python
Pytest
Requests
pytest-html
python-dotenv
Jenkins
Spring Boot REST API
```

## Folder Structure

```text
api-test-automation-suite/
|
|-- tests/
|   |-- test_health.py
|   |-- test_polls_api.py
|   `-- test_negative_cases.py
|
|-- utils/
|   `-- api_client.py
|
|-- config/
|   `-- test_data.json
|
|-- reports/
|
|-- conftest.py
|-- requirements.txt
|-- pytest.ini
|-- Jenkinsfile
`-- README.md
```

## Test Scenarios

Positive scenarios:

```text
Backend health check
Get all polls
Create a poll
Get poll by valid ID after creating a poll
Vote for a poll after creating a poll
```

Negative scenarios:

```text
Get poll using invalid poll ID
Create poll with empty payload
Create poll with empty question
Create poll with missing options
Vote using invalid poll ID or invalid vote payload
```

## How To Run Locally

Start your Spring Boot Polling Application first. By default, the test suite expects the backend to run at:

```text
http://localhost:8080
```

Create and activate a Python virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
pytest
```

## Run With Custom API URL

Use `BASE_URL` to run the same tests against local, dev, staging, Docker, Kubernetes, or Jenkins environments.

PowerShell:

```powershell
$env:BASE_URL="http://localhost:8080"
pytest
```

Command Prompt:

```bat
set BASE_URL=http://localhost:8080
pytest
```

Linux/macOS:

```bash
BASE_URL=http://localhost:8080 pytest
```

## HTML Test Report

The HTML report is generated automatically from `pytest.ini`:

```text
reports/api_test_report.html
```

You can also run the report command manually:

```bash
pytest --html=reports/api_test_report.html --self-contained-html
```

Open the generated report in a browser to view passed, failed, and skipped test details.

## Jenkins Pipeline

The included `Jenkinsfile` performs:

```text
Checkout code
Set up Python virtual environment
Install Python dependencies
Run Pytest API tests
Generate HTML report
Publish HTML report
```

In Jenkins, configure `BASE_URL` as an environment variable if your backend runs on a different host:

```text
BASE_URL=http://your-backend-host:8080
```

Required Jenkins plugin:

```text
HTML Publisher Plugin
```

After the build completes, Jenkins publishes:

```text
API Test Automation Report
```

## Useful Commands

Run tests with verbose output:

```bash
pytest -v
```

Run only health tests:

```bash
pytest tests/test_health.py
```

Run only negative tests:

```bash
pytest tests/test_negative_cases.py
```

Run tests against another environment:

```bash
BASE_URL=http://staging-api.example.com pytest
```

## Debugging Failed Tests

Each test prints useful response details:

```text
Endpoint
Status code
Response body
```

This helps debug backend validation failures in local runs and Jenkins reports.

## Resume Points

```latex
\resumeProjectHeading
{API Test Automation Suite $|$ Python, Pytest, REST APIs, Jenkins}
{https://github.com/Harsha2318/api-test-automation-suite}
\resumeItemListStart
\resumeItem{Built a Python-based API automation suite to validate Spring Boot REST endpoints, request payloads, status codes, and JSON responses.}
\resumeItem{Used Pytest fixtures, reusable API client utilities, and assertions to organize maintainable positive and negative test cases.}
\resumeItem{Implemented automated tests for health checks, poll creation, poll retrieval, invalid requests, and API error handling scenarios.}
\resumeItem{Generated HTML test reports and debugged failed cases using response logs, error messages, and API outputs.}
\resumeItem{Integrated API test execution with Jenkins to support backend validation during CI/CD workflows.}
\resumeItemListEnd
```

## Future Improvements

```text
Add Allure reports
Run tests inside Docker
Add GitHub Actions workflow
Add JSON schema validation
Load more test data from JSON files
Attach report screenshots to README
```
