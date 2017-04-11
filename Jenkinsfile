pipeline {
  agent {
    // run with the custom python slave
    // will dynamically provision a new pod on APPUiO
    label 'python'
  }
  
  stages {
    stage('test') {
      steps {
        echo 'Provisioning database...'
        openshiftScale(deploymentConfig='orders-test', replicaCount=1)
        echo 'Running tests...'
        sh 'pwd'
        sh 'python3.6 --version'
        // sh 'pip3.6 install -r requirements.txt'
        echo 'Removing database...'
        openshiftScale(deploymentConfig='orders-test', replicaCount=0)
      }
    }

    stage('build') {
      steps {
        echo 'Running S2I build...'
        sh 'pwd'
        sh 'python3.6 --version'
      }
    } 
  }
}