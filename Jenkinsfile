pipeline {
    agent any

    environment {
        IMAGE_NAME = "servicelink-app-image"
        TEST_CONTAINER = "test-runner-${env.BUILD_NUMBER}"
        APP_CONTAINER = "servicelink-web-app"
        AWS_IP = "13.63.34.67" 
    }

    stages {
        stage('Fetch Backend Code') {
            steps {
                checkout scm
                echo "Fetching backend folder from cloud-web..."
                sh "rm -rf temp_repo backend || true"
                sh "git clone https://github.com/groza9899-collab/cloud-web.git temp_repo"
                sh "cp -r temp_repo/backend ."
                sh "rm -rf temp_repo"
            }
        }

        stage('Lightweight Build') {
            steps {
                echo "Building the base image..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Mounting backend and running tests..."
                sh """
                docker run --name ${TEST_CONTAINER} -v ${WORKSPACE}/backend:/app/backend ${IMAGE_NAME} /bin/sh -c '
                python3 -m pip install uvicorn fastapi python-jose[cryptography] passlib[bcrypt] bcrypt sqlalchemy pydantic &&
                python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & 
                sleep 15 && 
                pytest test_service_link.py -v'
                """
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Deploying live to Port 3000..."
                sh "docker rm -f ${APP_CONTAINER} || true"
                // FIXED: Changed single " to triple \"\"\" to allow multi-line commands
                sh """
                docker run -d -p 3000:8000 --name ${APP_CONTAINER} -v ${WORKSPACE}/backend:/app/backend ${IMAGE_NAME} /bin/sh -c '
                python3 -m pip install uvicorn fastapi python-jose[cryptography] passlib[bcrypt] bcrypt sqlalchemy pydantic &&
                python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000'
                """
            }
        }
    }

    post {
        always {
            echo "Cleanup..."
            sh "docker rm -f ${TEST_CONTAINER} || true"
            mail to: 'qasimalik@gmail.com',
                 subject: "DevOps Assignment - Build #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
                 body: "Build #${env.BUILD_NUMBER} is ${currentBuild.currentResult}. URL: http://${AWS_IP}:3000"
        }
    }
}