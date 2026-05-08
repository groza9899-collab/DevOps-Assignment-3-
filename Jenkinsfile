pipeline {
    agent any

    environment {
        IMAGE_NAME = "servicelink-app-image"
        TEST_CONTAINER = "test-runner-${env.BUILD_NUMBER}"
        APP_CONTAINER = "servicelink-web-app"
        AWS_IP = "13.63.34.67" 
    }

    stages {
        stage('System Cleanup & Merge') {
            steps {
                echo "Cleaning up server space to prevent Build #14 crash..."
                // MAGIC FIX: Wipes old failed Docker data to free up Disk/RAM
                sh "docker system prune -f || true"
                sh "docker container prune -f || true"
                
                checkout scm
                sh "rm -rf temp_repo backend || true"
                sh "git clone https://github.com/groza9899-collab/cloud-web.git temp_repo"
                sh "cp -r temp_repo/backend ."
                sh "rm -rf temp_repo"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Injecting dependencies and building image..."
                // Using multiple echoes to ensure requirements.txt is formatted correctly
                sh "echo 'fastapi' > requirements.txt"
                sh "echo 'uvicorn[standard]' >> requirements.txt"
                sh "echo 'python-jose[cryptography]' >> requirements.txt"
                sh "echo 'passlib[bcrypt]' >> requirements.txt"
                sh "echo 'bcrypt' >> requirements.txt"
                sh "echo 'sqlalchemy' >> requirements.txt"
                sh "echo 'pydantic' >> requirements.txt"
                sh "echo 'pytest' >> requirements.txt"
                sh "echo 'selenium' >> requirements.txt"
                
                // REMOVED --no-cache to save system resources
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Starting server and running tests..."
                // Force install inside the container just in case build skips layers
                sh "docker run --name ${TEST_CONTAINER} ${IMAGE_NAME} /bin/sh -c 'python3 -m pip install uvicorn fastapi && python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & sleep 15 && pytest test_service_link.py -v'"
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Finalizing deployment on Port 3000..."
                sh "docker rm -f ${APP_CONTAINER} || true"
                sh "docker run -d -p 3000:8000 --name ${APP_CONTAINER} ${IMAGE_NAME} /bin/sh -c 'python3 -m pip install uvicorn fastapi && python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000'"
            }
        }
    }

    post {
        always {
            echo "Cleaning up build container..."
            sh "docker rm -f ${TEST_CONTAINER} || true"

            mail to: 'qasimalik@gmail.com',
                 subject: "DevOps Assignment - Build #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
                 body: "Hassaan's Build #${env.BUILD_NUMBER} Result: ${currentBuild.currentResult}. URL: http://${AWS_IP}:3000"
        }
    }
}