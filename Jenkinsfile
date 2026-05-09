pipeline {
    agent any
    environment {
        IMAGE_NAME = "servicelink-app-image"
        APP_CONTAINER = "servicelink-full-stack"
        AWS_IP = "13.63.34.67" 
    }
    stages {
        stage('Pull Code') {
            steps {
                sh "rm -rf temp_repo backend frontend || true"
                sh "git clone https://github.com/groza9899-collab/cloud-web.git temp_repo"
                // Copy backend if it exists
                sh "if [ -d temp_repo/backend ]; then cp -r temp_repo/backend .; fi"
                // Copy frontend if it exists, otherwise just use the root
                sh "if [ -d temp_repo/frontend ]; then cp -r temp_repo/frontend .; else cp -r temp_repo ./frontend; fi"
                sh "rm -rf temp_repo"
            }
        }
        stage('Build & Deploy') {
            steps {
                sh "docker rm -f ${APP_CONTAINER} || true"
                sh "docker build -t ${IMAGE_NAME} ."
                sh """
                docker run -d -p 3000:8000 --name ${APP_CONTAINER} \
                -v ${WORKSPACE}/backend:/app/backend \
                ${IMAGE_NAME} /bin/sh -c '
                pip install uvicorn fastapi python-jose[cryptography] passlib[bcrypt] bcrypt sqlalchemy pydantic python-multipart &&
                python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000'
                """
            }
        }
    }
    post {
        always {
            echo "Deployment link: http://${AWS_IP}:3000/docs"
        }
    }
}