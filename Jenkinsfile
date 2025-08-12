pipeline {
    agent { docker { image 'python:3.13.6-alpine3.22' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}