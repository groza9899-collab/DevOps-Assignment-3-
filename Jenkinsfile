pipeline {
    agent any

    environment {
        IMAGE_NAME = "servicelink-app-image"
        TEST_CONTAINER = "test-runner-${env.BUILD_NUMBER}"
        APP_CONTAINER = "servicelink-web-app"
        AWS_IP = "13.63.34.67" 
    }

    stages {
        stage('Checkout Code') {
            steps {
                // 1. Pull the tests from the current repo
                checkout scm
                
                // 2. MAGIC FIX: Pull the backend folder from your other repo automatically
                echo "Fetching application code from cloud-web..."
                sh "git clone https://github.com/groza9899-collab/cloud-web.git temp_repo"
                sh "cp -r temp_repo/backend ."
                sh "rm -rf temp_repo"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building image with website and tests..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Starting server and running 15 tests..."
                // Starts the FastAPI server in the background, waits 5 seconds, then runs pytest
                sh "docker run --name ${TEST_CONTAINER} ${IMAGE_NAME} /bin/sh -c 'uvicorn backend.main:app --host 0.0.0.0 --port 8000 & sleep 5 && pytest test_service_link.py -v'"
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Deploying live to Port 3000..."
                sh "docker rm -f ${APP_CONTAINER} || true"
                // Map AWS Port 3000 to App Port 8000
                sh "docker run -d -p 3000:8000 --name ${APP_CONTAINER} ${IMAGE_NAME} uvicorn backend.main:app --host 0.0.0.0 --port 8000"
            }
        }
    }

    post {
        always {
            echo "Cleaning up..."
            sh "docker rm -f ${TEST_CONTAINER} || true"

            mail to: 'qasimalik@gmail.com',
                 subject: "DevOps Assignment - Build #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
                 body: """The pipeline has completed.
Status: ${currentBuild.currentResult}
Deployment URL: http://${AWS_IP}:3000"""
        }
    }
}