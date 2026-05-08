pipeline {
    agent any

    environment {
        // Use a pre-built image to bypass the 'Killed' error during Chrome install
        IMAGE_NAME = "joyzoursky/python-selenium:3.11-chrome"
        TEST_CONTAINER = "test-runner-${env.BUILD_NUMBER}"
        APP_CONTAINER = "servicelink-web-app"
        AWS_IP = "13.63.34.67" 
    }

    stages {
        stage('Merge Repositories') {
            steps {
                echo "Fetching your application code..."
                checkout scm
                // Clear old folders and grab fresh code from your backend repo
                sh "rm -rf temp_repo backend || true"
                sh "git clone https://github.com/groza9899-collab/cloud-web.git temp_repo"
                sh "cp -r temp_repo/backend ."
                sh "rm -rf temp_repo"
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running 15 Tests inside pre-built Selenium container..."
                // 1. We create the requirements file on the fly
                sh "echo 'fastapi\nuvicorn[standard]\npython-jose[cryptography]\npasslib[bcrypt]\nbcrypt\nsqlalchemy\npydantic\npytest\nselenium' > requirements.txt"
                
                // 2. We run the container, install your app's specific tools, and run the server + tests
                sh """
                docker run --name ${TEST_CONTAINER} -v ${WORKSPACE}:/app -w /app ${IMAGE_NAME} /bin/sh -c '
                pip install -r requirements.txt && 
                python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & 
                sleep 15 && 
                pytest test_service_link.py -v'
                """
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Deploying to AWS Port 3000..."
                sh "docker rm -f ${APP_CONTAINER} || true"
                
                // Map your open Port 3000 to the App Port 8000
                sh """
                docker run -d -p 3000:8000 --name ${APP_CONTAINER} -v ${WORKSPACE}:/app -w /app ${IMAGE_NAME} /bin/sh -c '
                pip install -r requirements.txt && 
                python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000'
                """
                
                echo "Success! View your site at http://${AWS_IP}:3000"
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

The pipeline has finished successfully.
Status: ${currentBuild.currentResult}
Deployment: http://${AWS_IP}:3000"""
        }
    }
}