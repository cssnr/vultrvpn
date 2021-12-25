#!/usr/bin/env groovy

@Library('jenkins-libraries')_

pipeline {
    agent {
        label 'manager'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr:'5'))
        timeout(time: 1, unit: 'HOURS')
    }
    environment {
        DISCORD_ID = "smashed-alerts"
        COMPOSE_FILE = "docker-compose-swarm.yml"

        BUILD_CAUSE = getBuildCause()
        VERSION = getVersion("${GIT_BRANCH}")
        GIT_ORG = getGitGroup("${GIT_URL}")
        GIT_REPO = getGitRepo("${GIT_URL}")
        BASE_NAME = "${GIT_ORG}-${GIT_REPO}"
        SERVICE_NAME = "${BASE_NAME}"
        NFS_HOST = "nfs01.cssnr.com"
    }
    stages {
        stage('Init') {
            steps {
                echo "\n--- Build Details ---\n" +
                        "GIT_URL:       ${GIT_URL}\n" +
                        "JOB_NAME:      ${JOB_NAME}\n" +
                        "COMPOSE_FILE:  ${COMPOSE_FILE}\n" +
                        "SERVICE_NAME:  ${SERVICE_NAME}\n" +
                        "NFS_HOST:      ${NFS_HOST}\n" +
                        "BUILD_CAUSE:   ${BUILD_CAUSE}\n" +
                        "GIT_BRANCH:    ${GIT_BRANCH}\n" +
                        "VERSION:       ${VERSION}\n"
                verifyBuild()
                sendDiscord("${DISCORD_ID}", "Pipeline Started by: ${BUILD_CAUSE}")
                getConfigs("${SERVICE_NAME}")   // use this to get service configs from deploy-configs
            }
        }
        stage('Dev Deploy') {
            when {
                allOf {
                    not { branch 'master' }
                }
            }
            environment {
                STACK_NAME = "dev-${SERVICE_NAME}"
                NFS_DIRECTORY = "/data/docker/${STACK_NAME}"
                TRAEFIK_HOST = "`vultrvpn-dev.sapps.me`"
                ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/dev.env"
            }
            steps {
                echo "\n--- Starting Dev Deploy ---\n" +
                        "STACK_NAME:        ${STACK_NAME}\n" +
                        "NFS_DIRECTORY:     ${NFS_DIRECTORY}\n" +
                        "TRAEFIK_HOST:      ${TRAEFIK_HOST}\n" +
                        "ENV_FILE:          ${ENV_FILE}\n"
                sendDiscord("${DISCORD_ID}", "Dev Deploy Started")
                setupNfs("${STACK_NAME}")
                updateCompose("${COMPOSE_FILE}", "STACK_NAME", "${STACK_NAME}")
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
                sendDiscord("${DISCORD_ID}", "Dev Deploy Finished")
            }
        }
        stage('Prod Deploy') {
            when {
                allOf {
                    branch 'master'
                    triggeredBy 'UserIdCause'
                }
            }
            environment {
                STACK_NAME = "prod-${SERVICE_NAME}"
                NFS_DIRECTORY = "/data/docker/${STACK_NAME}"
                TRAEFIK_HOST = "`vultrvpn.sapps.me`"
                ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/prod.env"
            }
            steps {
                echo "\n--- Starting Prod Deploy ---\n" +
                        "STACK_NAME:        ${STACK_NAME}\n" +
                        "NFS_DIRECTORY:     ${NFS_DIRECTORY}\n" +
                        "TRAEFIK_HOST:      ${TRAEFIK_HOST}\n" +
                        "ENV_FILE:          ${ENV_FILE}\n"
                sendDiscord("${DISCORD_ID}", "Prod Deploy Started")
                setupNfs("${STACK_NAME}")
                updateCompose("${COMPOSE_FILE}", "STACK_NAME", "${STACK_NAME}")
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
                sendDiscord("${DISCORD_ID}", "Prod Deploy Finished")
            }
        }
    }
    post {
        always {
            cleanWs()
            script { if (!env.INVALID_BUILD) {
                sendDiscord("${DISCORD_ID}", "Pipeline Complete: ${currentBuild.currentResult}")
            } }
        }
    }
}
