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

        // scale the ephemeral orders-test database to 1 replica
        openshiftScale(depCfg: 'orders-test', replicaCount: '1')

        // sleep for 20s to give the db chance to initialize
        sleep 20

        echo 'Installing dependencies...'

        // install the application requirements
        // wrap([$class: 'CacheWrapper', 'path': '.pip']) {
        // sh 'pip3.6 install --user -r requirements.txt --download-cache=.pip'
        // }
        sh 'pip3.6 install --user -r requirements.txt'

        echo 'Running tests...'

        // run the application tests with verbose output
        sh 'python3.6 -m unittest wsgi_test --verbose'
      }

      post {
        always {
          echo 'Removing database...'

          // scale the ephemeral orders-test database to 0 replicas
          // as it is ephemeral, all data will be lost
          openshiftScale(depCfg: 'orders-test', replicaCount: '0')
        }
      }
    }

    stage('deploy-staging') {
      agent any

      steps {
        echo 'Running S2I build...'

        // start a new openshift build
        openshiftBuild(bldCfg: 'orders-staging')

        echo 'Replacing OC config...'

        // replace the openshift config
        script {
          openshift.withCluster() {
            openshift.replace('-f', 'docker/openshift/*')
          }
        }

        echo 'Starting new deployment...'

        // trigger a new openshift deployment
        openshiftDeploy(depCfg: 'orders-staging')
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

        // tag the latest image as stable
        openshiftTag(srcStream: 'orders', srcTag: 'latest', destStream: 'orders', destTag: 'stable')

        echo 'Replacing OC config...'

        // TODO: replace the openshift config

        echo 'Starting new deployment...'

        // trigger a new openshift deployment
        openshiftDeploy(depCfg: 'orders-preprod')
      }

      when {
        // TODO: only do this on a new release / git tag
        // this is blocked by an issue with jenkins
        branch 'preprod'
      }
    }

    stage('deploy-prod') {
      agent any

      steps {
        echo 'Promoting to prod...'

        // tag the stable image as live
        openshiftTag(srcStream: 'orders', srcTag: 'stable', destStream: 'orders', destTag: 'live')

        echo 'Replacing OC config...'

        // TODO: replace the openshift config

        echo 'Starting new deployment...'

        // trigger a new openshift deployment
        openshiftDeploy(depCfg: 'orders-prod')
      }

      when {
        // TODO: only do this on a new release / git tag
        // this is blocked by an issue with jenkins
        branch 'prod'
      }
    }
  }
}