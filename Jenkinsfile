pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // Fetches your code from GitHub as required
                git url: 'https://github.com/groza9899-collab/DevOps-Assignment-3-.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t servicelink-test-image .'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                // Executes the 15 tests in a containerized environment
                sh 'docker run --name test-container-run servicelink-test-image'
            }
        }
    }

    post {
        always {
            // Mandatory requirement: Email test results to the collaborator
            mail to: 'qasimalik@gmail.com',
                 subject: "DevOps-Assign3: Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                 body: """The pipeline for ${env.JOB_NAME} has finished.
                 Result: ${currentBuild.currentResult}
                 Build URL: ${env.BUILD_URL}
                 15 Selenium Tests executed."""
            
            // Cleanup to ensure the next build doesn't fail
            sh 'docker rm -f test-container-run'
        }
    }
}