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
        // sh 'pip3.6 install --user -r requirements.txt'
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