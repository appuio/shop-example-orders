pipeline {
  agent any
  
  stages {
    stage('test') {
      agent {
        // run with the custom python slave
        // will dynamically provision a new pod on APPUiO
        label 'python'
      }
      steps {
        echo 'Running tests...'
        sh 'pwd'
        sh 'python3.6 --version'
        sh 'python3.6 app_test.py'
      }
    }

    stage('build') {
      agent any
      steps {
        echo 'Running S2I build...'
        // TODO: start the S2I build on APPUiO
      }
    } 
  }
}