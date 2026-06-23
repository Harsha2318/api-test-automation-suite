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
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Python Virtual Environment') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest API Tests and Generate HTML Report') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                    . $VENV_DIR/bin/activate
                    pytest --html=reports/api_test_report.html --self-contained-html
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
