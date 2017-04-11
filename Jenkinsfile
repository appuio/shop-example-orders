pipeline {
  agent any
  
  stages {
    stage('test') {
      agent {
        // run with the custom python slave
        // will dynamically provision a new pod on APPUiO
        label 'python'
      }

      environment {
        DB_HOSTNAME = 'orders-test'
        DB_USERNAME = 'orders'
        DB_PASSWORD = 'secret'
        DB_DATABASE = 'orders'
      }

      steps {
        echo 'Provisioning database...'
        openshiftScale(depCfg: 'orders-test', replicaCount: '1')
          /*openshift.withCluster() {
            openshift.raw('scale', 'dc', 'orders-test', '--replicas=1')
          }*/
        echo 'Running tests...'
        sh 'env'
        sh 'pwd'
        // sh 'ping orders-test'
        sh 'ls -la /usr/local/bin'
        sh 'python3.6 --version'
        // install the application requirements
        sh 'pip3.6 install -r requirements.txt'
        // run the application tests
        sh 'python app_test.py'
      }

      post {
        always {
          echo 'Removing database...'
          openshiftScale(depCfg: 'orders-test', replicaCount: '0')
            /*openshift.withCluster() {
              openshift.raw('scale', 'dc', 'orders-test', '--replicas=0')
            }*/
        }
      }
    }

    stage('build') {
      agent any

      steps {
        echo 'Running S2I build...'
        sh 'pwd'
        sh 'python3.6 --version'
        // start a new openshift build
        // openshiftBuild('orders-staging')
      }

      when {
        // TODO: don't do this on a new release / git tag
        branch 'master'
      }
    }

    stage('deploy-preprod') {
      agent any

      steps {
        echo 'Promoting to preprod...'
      }

      // when {
        // TODO: only do this on a new release / git tag
      // }
    }

    stage('deploy-prod') {
      agent any

      steps {
        echo 'Promoting to prod...'
      }

      // when {
        // TODO: only do this on manual intervention
      // }
    }
  }
}