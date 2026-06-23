pipeline {
    agent any

    parameters {
        string(
            name: 'BASE_URL',
            defaultValue: 'http://localhost:8080',
            description: 'Base URL of the Spring Boot Polling Application backend'
        )
    }

    environment {
        VENV_DIR = ".venv"
        JENKINS_ENV_FILE = ".jenkins-python-env"
        API_TIMEOUT = "5"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Python Environment') {
            steps {
                sh '''
                set +e
                python3 --version
                rm -rf "$VENV_DIR"
                python3 -m venv "$VENV_DIR"
                VENV_STATUS=$?
                set -e

                if [ "$VENV_STATUS" -eq 0 ]; then
                    echo "USE_VENV=true" > "$JENKINS_ENV_FILE"
                    echo "Python virtual environment created successfully."
                else
                    echo "USE_VENV=false" > "$JENKINS_ENV_FILE"
                    echo "Python venv is not available on this Jenkins agent."
                    echo "Falling back to user-level pip installation."
                fi
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                . "./$JENKINS_ENV_FILE"

                if [ "$USE_VENV" = "true" ]; then
                    . "$VENV_DIR/bin/activate"
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                else
                    if ! python3 -m pip --version; then
                        echo "python3-pip is missing on the Jenkins agent."
                        echo "Bootstrapping pip for the Jenkins user."

                        if command -v curl >/dev/null 2>&1; then
                            curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
                        elif command -v wget >/dev/null 2>&1; then
                            wget -q https://bootstrap.pypa.io/get-pip.py -O get-pip.py
                        else
                            echo "Neither curl nor wget is available."
                            echo "Install Python tooling once with: sudo apt install python3-pip python3-venv curl -y"
                            exit 1
                        fi

                        python3 get-pip.py --user --break-system-packages || python3 get-pip.py --user
                    fi

                    export PATH="$HOME/.local/bin:$PATH"
                    python3 -m pip install --user --break-system-packages -r requirements.txt || python3 -m pip install --user -r requirements.txt
                fi
                '''
            }
        }

        stage('Verify API Availability') {
            steps {
                sh '''
                . "./$JENKINS_ENV_FILE"

                if [ "$USE_VENV" = "true" ]; then
                    . "$VENV_DIR/bin/activate"
                else
                    export PATH="$HOME/.local/bin:$PATH"
                fi

                python3 - <<'PY'
import os
import sys
import urllib.error
import urllib.request

base_url = os.environ.get("BASE_URL", "http://localhost:8080").rstrip("/")
health_url = f"{base_url}/actuator/health"
timeout = int(os.environ.get("API_TIMEOUT", "5"))

print(f"Checking API availability: {health_url}")

try:
    with urllib.request.urlopen(health_url, timeout=timeout) as response:
        status_code = response.getcode()
        body = response.read().decode("utf-8", errors="replace")
        print(f"API health status code: {status_code}")
        print(f"API health response: {body}")
        if status_code >= 400:
            sys.exit(f"API health check returned HTTP {status_code}")
except (urllib.error.URLError, TimeoutError, OSError) as error:
    print("")
    print("API is not reachable from the Jenkins agent.")
    print(f"BASE_URL: {base_url}")
    print(f"Error: {error}")
    print("")
    print("Check that:")
    print("1. The Spring Boot backend is running.")
    print("2. BASE_URL uses the correct IP address reachable from Jenkins.")
    print("3. The backend listens on 0.0.0.0, not only localhost.")
    print("4. Firewall allows inbound traffic on port 8080.")
    sys.exit(1)
PY
                '''
            }
        }

        stage('Run Pytest API Tests and Generate HTML Report') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                    . "./$JENKINS_ENV_FILE"

                    if [ "$USE_VENV" = "true" ]; then
                        . "$VENV_DIR/bin/activate"
                        pytest --html=reports/api_test_report.html --self-contained-html
                    else
                        export PATH="$HOME/.local/bin:$PATH"
                        python3 -m pytest --html=reports/api_test_report.html --self-contained-html
                    fi
                    '''
                }
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'api_test_report.html',
                    reportName: 'API Test Automation Report'
                ])
            }
        }
    }
}
