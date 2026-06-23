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
                        echo "Install it once with: sudo apt install python3-pip python3-venv -y"
                        exit 1
                    fi

                    python3 -m pip install --user --break-system-packages -r requirements.txt
                fi
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
