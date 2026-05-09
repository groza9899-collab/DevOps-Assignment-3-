pipeline {
    agent any

    environment {
        IMAGE_NAME = "servicelink-app-image"
        APP_CONTAINER = "servicelink-full-stack"
        AWS_IP = "13.63.34.67" 
    }

    stages {
        stage('Pull Full Code') {
            steps {
                checkout scm
                // Pulling EVERYTHING so we have both React and Python
                sh "rm -rf temp_repo backend frontend || true"
                sh "git clone https://github.com/groza9899-collab/cloud-web.git temp_repo"
                sh "cp -r temp_repo/backend ."
                sh "cp -r temp_repo/frontend ."
                sh "rm -rf temp_repo"
            }
        }

        stage('Build Frontend Assets') {
            steps {
                echo "Building the React UI..."
                sh "cd frontend && npm install --production && npm run build"
            }
        }

        stage('Deploy Full Stack') {
            steps {
                echo "Deploying live to: http://${AWS_IP}:3000"
                sh "docker rm -f ${APP_CONTAINER} || true"
                sh "docker build -t ${IMAGE_NAME} ."
                sh """
                docker run -d -p 3000:8000 --name ${APP_CONTAINER} \
                -v ${WORKSPACE}/backend:/app/backend \
                -v ${WORKSPACE}/frontend:/app/frontend \
                ${IMAGE_NAME} /bin/sh -c '
                pip install uvicorn fastapi python-jose[cryptography] passlib[bcrypt] bcrypt sqlalchemy pydantic python-multipart &&
                python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000'
                """
            }
        }
    }

    post {
        success {
            mail to: 'qasimalik@gmail.com',
                 subject: "DevOps Assignment Submission - Hassaan",
                 body: "Sir,\n\nThe full-stack deployment is successful.\nURL: http://${AWS_IP}:3000\nSwagger: http://${AWS_IP}:3000/docs"
        }
        failure {
            echo "Build failed. Check the logs."
        }
    }
}