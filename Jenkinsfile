pipeline {
    agent any

    environment {
        // Questo ID deve corrispondere a quello creato in Jenkins Credentials
        DOCKERHUB_REGISTRY = "docker.io"
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
        // CAMBIA 'giacomo12305' con il tuo vero nome utente Docker Hub
        APP_NAME = "tuo-username/data-factory-app"
    }

    stages {
        stage('Cloning Git') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Jenkins builda l'immagine usando il Dockerfile nella cartella /app
                    sh "docker build -t ${APP_NAME}:latest ./app"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Login e Push su Docker Hub
                    sh "echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin ${DOCKERHUB_REGISTRY}"
                    sh "docker push ${APP_NAME}:latest"
                }
            }
        }
    }
}
