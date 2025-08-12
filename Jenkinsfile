pipeline {
    agent { docker { image 'python:3.12.11-alpine3.22' } }
    environment {
        PORT = '8006'
        HOST = '0.0.0.0'
        FRONTEND_URL = credentials('frontend-url')
        TOKEN_LIFETIME_SECOND = credentials('token-lifetime-second')
    }
    stages {
        stage('Build Production') {
            steps {
                sh 'python -m venv env'
                sh '. ./env/bin/activate'
                sh 'pip install -r requirements.txt'
                sh 'python manage.py migrate'
            }
        }
        stage('Deploy Production') {
            steps {
                sh 'python manage.py runserver ${HOST}:${PORT}'
            }
        }
    }
}