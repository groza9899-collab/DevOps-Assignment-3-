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
                echo "Fetching application code and injecting dependencies..."
                sh "git clone https://github.com/groza9899-collab/cloud-web.git temp_repo"
                sh "cp -r temp_repo/backend ."
                
                // MAGIC FIX: Inject all backend requirements into the build file
                sh "echo 'fastapi\nuvicorn[standard]\npython-jose[cryptography]\npasslib[bcrypt]\nbcrypt\nsqlalchemy\npydantic' >> requirements.txt"
                
                sh "rm -rf temp_repo"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building image (No Cache to ensure new dependencies)..."
                // Added --no-cache to force Docker to actually install the new requirements
                sh "docker build --no-cache -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Starting server and running tests..."
                // Starts server, waits 15 seconds for stability, then runs tests
                sh "docker run --name ${TEST_CONTAINER} ${IMAGE_NAME} /bin/sh -c 'python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & sleep 15 && pytest test_service_link.py -v'"
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Deploying live to Port 3000..."
                sh "docker rm -f ${APP_CONTAINER} || true"
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
                 body: """Hassaan here.

The pipeline for Build #${env.BUILD_NUMBER} has finished.
Status: ${currentBuild.currentResult}
Deployment URL: http://${AWS_IP}:3000"""
        }
    }
}