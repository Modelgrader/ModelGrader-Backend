pipeline {
    agent any
    environment {
        ENV_FILE=credentials("grader-backend-${params.Environment}")
        IMAGE_NAME="grader-backend-${params.Environment}"
        CONTAINER_NAME="grader-backend-${params.Environment}-container"
    }
    stages {
        stage("Setup Environment") {
            steps {
                echo "Create environment file with credentials"
                sh """
                cp $ENV_FILE .env
                """
            }
        }
        stage("Build Image") {
            steps {
                echo "Build Docker image: ${IMAGE_NAME}"
                sh """
                docker build -t $IMAGE_NAME:latest .
                """
            }
        }
        stage("Run Container") {
            steps {
                echo "Run Docker container: ${CONTAINER_NAME} on port: ${params.PORT}"
                sh """
                docker stop $CONTAINER_NAME || true && docker rm $CONTAINER_NAME || true
                docker run -d --name $CONTAINER_NAME -p ${params.PORT}:8000 $IMAGE_NAME:latest
                """
            }
        }
    }
}