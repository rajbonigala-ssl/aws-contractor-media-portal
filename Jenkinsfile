@Library('ciinabox') _

echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
echo "Running ${env.BUILD_NUMBER} on ${env.JENKINS_URL}"

pipeline{
    environment {
        STACK_NAME = 'ContractorMediaPortal'
        REGION = 'ap-southeast-2'
        ECR_REPO = '225638025013.dkr.ecr.ap-southeast-2.amazonaws.com'
        OPS_ACCOUNT_ID = '225638025013'
        PROJECT_NAME = 'servicestream'
        AWS_REGION = 'ap-southeast-2'
        TEMPLATE_NAME = 'cfn.yaml'
        TEMPLATE_EXPORT_NAME = 'output.yaml'
        S3_BUCKET = 'source.aws.ssdev'
        CF_TEMPLATE_URL = 'https://s3-ap-southeast-2.amazonaws.com/source.aws.ssdev/jenkins/'
        DEV_ACCOUNT_ID = '638325003329'
        TEST_ACCOUNT_ID = '638325003329'
        UAT_ACCOUNT_ID = '708477449728'
        PROD_ACCOUNT_ID = '708477449728'
        CIINABOX_ROLE = 'ciinabox'
        DEV_ROLE_ARN = "arn:aws:iam::638325003329:role/ciinabox"
        TEST_ROLE_ARN = "arn:aws:iam::638325003329:role/ciinabox"
        UAT_ROLE_ARN = "arn:aws:iam::708477449728:role/ciinabox"
        PROD_ROLE_ARN = "arn:aws:iam::708477449728:role/ciinabox"
        S3_BUILD_LOCATION = "s3://${env.S3_BUCKET}/cloudformation/jenkins/${env.STACK_NAME}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}"
        S3_BUILD_KEYPATH = "cloudformation/jenkins/${env.STACK_NAME}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}"
        HOME = '/tmp'
        
        CODEDEPLOY_ZIP = "codedeploy.${env.BUILD_ID}.zip"
        S3_DEPLOY = "ss.contractormediaportal"
    }
    agent {
        dockerfile {
            filename 'Dockerfile.build'
        }
    }
    stages{
        stage('Prepare') {
            steps {
                script {

                    if (env.BRANCH_NAME == 'develop') {
                        env.AWS_ENV = 'dev'
                        env.ROLE_ARN = "${env.DEV_ROLE_ARN}"
                        env.CFN_ENV = 'DEV'
                        env.ASPNETCORE_ENVIRONMENT = 'Development'

                    } else if (env.BRANCH_NAME == 'test') {
                        env.AWS_ENV = 'test'
                        env.ROLE_ARN = "${env.TEST_ROLE_ARN}"
                        env.CFN_ENV = 'TEST'
                        env.ASPNETCORE_ENVIRONMENT = 'Test'

                    } else if (env.BRANCH_NAME == 'uat') {
                        env.AWS_ENV = 'uat'
                        env.ROLE_ARN = "${env.UAT_ROLE_ARN}"
                        env.CFN_ENV = 'UAT'
                        env.ASPNETCORE_ENVIRONMENT = 'UAT'
                        timeout(time: 2, unit: "HOURS") {
                        input message: 'Are you sure you want to deploy to UAT?', ok: 'Yes'
                        }

                    } else if (env.BRANCH_NAME == 'master') {
                        env.AWS_ENV = 'prod'
                        env.ROLE_ARN = "${env.PROD_ROLE_ARN}"
                        env.CFN_ENV = 'PROD'
                        env.ASPNETCORE_ENVIRONMENT = 'Production'
                        timeout(time: 2, unit: "HOURS") {
                        input message: 'Are you sure you want to deploy to PRODUCTION?', ok: 'Yes'
                        }

                    } else {
                        
                        error "Unknown GIT branch, cannot continue."
                        
                    }
                    
                    sh "set"

                    }
            }
        }
        stage('Build') {
            steps {
                println "Building JOB_NAME: ${env.JOB_NAME}, BUILD_ID: ${env.BUILD_ID}"
                println "Git branch: ${env.BRANCH_NAME} for AWS env: ${env.AWS_ENV}"

                println "BUILD_URL: ${env.BUILD_URL}"
                println "WORKSPACE: ${env.WORKSPACE}"

                println "ROLE_ARN: ${env.ROLE_ARN}"
                println "STACK_NAME: ${env.STACK_NAME}"
                println "PROJECT_URL: ${env.PROJECT_URL}"

                sh "dotnet --version"
                
                println "Build "
                
                sh '''
                #!/bin/bash
                

                SESSION_NAME="jenkins"
                OUTPUT_TRANSFORM="--query Credentials.[AccessKeyId,SecretAccessKey,SessionToken] --output text"
                ASSUME_CMD="aws sts assume-role --output text --role-arn $ROLE_ARN --role-session-name $SESSION_NAME $OUTPUT_TRANSFORM"
                RESULTS=`$ASSUME_CMD`
                AWS_ACCESS_KEY_ID_ENV=`echo $RESULTS | cut -d' ' -f1`
                AWS_SECRET_ACCESS_KEY_ENV=`echo $RESULTS | cut -d' ' -f2`
                AWS_SESSION_TOKEN_ENV=`echo $RESULTS | cut -d' ' -f3`
                echo -n $AWS_ACCESS_KEY_ID_ENV > AWS_ACCESS_KEY_ID_FILE
                echo -n $AWS_SECRET_ACCESS_KEY_ENV > AWS_SECRET_ACCESS_KEY_FILE
                echo -n $AWS_SESSION_TOKEN_ENV > AWS_SESSION_TOKEN_FILE

                '''

                sh "cd ~/aws-contractor-media-portal/aws_contractor_media_portal"
                sh "python3 cdk synth"

            }
        }
    }

}