pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t simple-python-app:latest .'
            }
        }
        
        stage('Stop Old Container') {
            steps {
                echo 'Stopping old container...'
                sh 'docker stop simple-python-app || true'
                sh 'docker rm simple-python-app || true'
            }
        }
        
        stage('Deploy Container') {
            steps {
                echo 'Deploying new container...'
                sh 'docker run -d -p 9090:9090 --name simple-python-app simple-python-app:latest'
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                sh 'sleep 5 && curl http://localhost:9090/health'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
