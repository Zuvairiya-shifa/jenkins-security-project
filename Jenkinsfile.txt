pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/zuvairiya-shifa/jenkins-security-project.git'
            }
        }

        stage('Setup') {
            steps {
                bat '''
                    python -m venv venv
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                    venv\\Scripts\\python.exe -m pip install bandit pip-audit
                '''
            }
        }

        stage('Build') {
            steps {
                bat 'echo Application build completed'
            }
        }

        stage('Testing') {
            steps {
                bat 'venv\\Scripts\\python.exe -m pytest -v'
            }
        }

        stage('SAST - Bandit') {
            steps {
                bat '''
                    venv\\Scripts\\python.exe -m bandit -r . -x venv -f json -o bandit-report.json
                '''
            }
        }

        stage('SCA - pip-audit') {
            steps {
                bat '''
                    venv\\Scripts\\python.exe -m pip_audit -r requirements.txt -f json -o pip-audit-report.json
                '''
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: '*.json',
                allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Security pipeline execution completed'
        }
    }
}