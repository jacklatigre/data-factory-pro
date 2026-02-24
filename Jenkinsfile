pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24.0.5-dind
    securityContext:
      privileged: true
    volumeMounts:
    - name: dind-storage
      mountPath: /var/lib/docker
  volumes:
  - name: dind-storage
    emptyDir: {}
"""
        }
    }

    environment {
        DOCKERHUB_REGISTRY = "docker.io"
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
        // QUI METTI IL TUO USERNAME VERO
        APP_NAME = "giacomo12305/data-factory-app" 
    }

    stages {
        stage('Build & Push') {
            steps {
                // Usiamo il container 'docker' definito sopra
                container('docker') {
                    script {
                        // Aspetta che Docker sia pronto
                        sh "while ! docker ps; do sleep 1; done"
                        
                        // Build dell'immagine
                        sh "docker build -t ${APP_NAME}:latest ./app"
                        
                        // Login e Push
                        sh "echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin ${DOCKERHUB_REGISTRY}"
                        sh "docker push ${APP_NAME}:latest"
                    }
                }
            }
        }
    }
}
