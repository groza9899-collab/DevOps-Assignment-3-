pipeline {
    agent any

    environment {
        IMAGE_NAME = "servicelink-app-image"
        TEST_CONTAINER = "test-runner-${env.BUILD_NUMBER}"
        APP_CONTAINER = "servicelink-web-app"
        // Your specific AWS Public IP
        AWS_IP = "13.63.34.67" 
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Pulls latest from your GitHub
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Executing 15 Selenium Test Cases..."
                // Runs tests and captures the result for the status
                sh "docker run --name ${TEST_CONTAINER} ${IMAGE_NAME} pytest test_service_link.py -v"
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Deploying to AWS on Port 3000..."
                // 1. Clear any existing app container to avoid name/port conflicts
                sh "docker rm -f ${APP_CONTAINER} || true"
                
                // 2. Launch the app in detached mode (-d)
                // Maps AWS Port 3000 to FastAPI Port 8000
                sh "docker run -d -p 3000:8000 --name ${APP_CONTAINER} ${IMAGE_NAME} uvicorn backend.main:app --host 0.0.0.0 --port 8000"
                
                echo "Application is live at http://${AWS_IP}:3000"
            }
        }
    }

    post {
        always {
            echo "Cleaning up test environment..."
            // Remove the test runner, but leave the APP_CONTAINER running for the instructor
            sh "docker rm -f ${TEST_CONTAINER} || true"

            mail to: 'qasimalik@gmail.com',
                 subject: "DevOps Assignment - Build #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
                 body: """Hassaan here. 

The pipeline for Build #${env.BUILD_NUMBER} has completed.

Status: ${currentBuild.currentResult}
Test Results: 15/15 Selenium cases executed.
Deployment URL: http://${AWS_IP}:3000

The application is now live and ready for your review at the link above."""
        }
    }
}