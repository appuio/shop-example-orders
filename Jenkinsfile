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
        openshiftScale(deploymentConfig: 'orders-test', replicaCount: 1)
          /*openshift.withCluster() {
            openshift.raw('scale', 'dc', 'orders-test', '--replicas=1')
          }*/
        echo 'Running tests...'
        sh 'env'
        sh 'pwd'
        sh 'ping orders-test'
        sh 'python3.6 --version'
        // install the application requirements
        sh 'pip3.6 install -r requirements.txt'
        // run the application tests
        sh 'python app_test.py'
      }
      post {
        always {
          echo 'Removing database...'
          script {
            openshiftScale(deploymentConfig: 'orders-test', replicaCount: 0)
            /*openshift.withCluster() {
              openshift.raw('scale', 'dc', 'orders-test', '--replicas=0')
            }*/
          }
        }
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