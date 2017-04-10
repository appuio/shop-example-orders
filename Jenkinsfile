pipeline {
  agent any
  
  stages {
    stage('test') {
      agent {
        // run with the custom python slave
        label 'python'
      }
      steps {
        echo 'Running tests...'
        sh 'pwd'
        sh 'python --version'
        // TODO: run tests
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