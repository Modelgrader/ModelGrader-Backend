pipeline {
    agent { docker { image 'python:3.12.11-alpine3.22' } }
    stages {
        stage('Build Production') {
            steps {
                sh 'python -m venv env'
                sh '. ./env/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Deploy Production') {
            steps {
                sh 'pm2 start start-prod.sh --name "grader-prod"'
                sh 'pm2 save'
            }
        }
    }
}