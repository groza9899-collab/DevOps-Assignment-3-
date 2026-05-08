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
                checkout scm
                echo "Fetching application code from cloud-web..."
                sh "git clone https://github.com/groza9899-collab/cloud-web.git temp_repo"
                sh "cp -r temp_repo/backend ."
                sh "rm -rf temp_repo"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building image..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Starting server and running tests..."
                // FIX: Use 'python -m uvicorn' instead of just 'uvicorn' to ensure it is found
                sh "docker run --name ${TEST_CONTAINER} ${IMAGE_NAME} /bin/sh -c 'python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & sleep 10 && pytest test_service_link.py -v'"
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Deploying live to Port 3000..."
                sh "docker rm -f ${APP_CONTAINER} || true"
                // FIX: Using 'python -m uvicorn' here as well
                sh "docker run -d -p 3000:8000 --name ${APP_CONTAINER} ${IMAGE_NAME} python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
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