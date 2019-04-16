pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:3.7-alpine3.8'
                }
            }
            steps {
                sh 'python -m py_compile boom_bot.py'
            }
        }
    }
}