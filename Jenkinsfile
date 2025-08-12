pipeline {
    agent { docker { image 'python:3.13.6-alpine3.22' } }
    stages {
        stage('Build Development') {
            steps {
                sh 'git checkout dev'
                sh 'python -m venv env-dev'
                sh '. ./env/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Deploy Development') {
            steps {
                sh 'pm2 start start-dev.sh --name "grader-dev"'
                sh 'pm2 save'
            }
        }
    }
}