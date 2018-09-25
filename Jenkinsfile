pipeline {
    agent any 
    stages {
        stage('Checkout') { 
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/myersb89/Alexa-Recipe-Tracker.git']]])
            }
        }
        stage('Build') { 
            steps {
                bat '''REM Build the requirements in a virtual environment
                    virtualenv venv
                    .\\venv\\Scripts\\pip.exe install -r requirements.txt''' 
            }
        }
        stage('Test') { 
            steps {
                bat '''REM Run the testing scripts
                .\\venv\\Scripts\\pytest.exe'''
            }
        }
        stage('Deploy') { 
            steps {
                bat '''REM Build the .zip file
                    xcopy /y recipeTracker.py venv\\Lib\\site-packages
                    mkdir builds
                    "C:\\Program Files\\7-Zip\\7z.exe" a -tzip "builds\\recipeTracker.zip" ".\\venv\\Lib\\site-packages\\*"'''
                    
                withAWS(region:'us-east-1',credentials:'1000') {
                    s3Upload(file:'builds/recipetracker.zip', bucket:'myersb89-recipetracker', path:'recipetracker.zip')
                }   
            }
        }
    }
}