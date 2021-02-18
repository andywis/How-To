# Jenkinsfile examples

(Jun 2020)

Below is an example Jenkinsfile. It demonstrates a few things:
* Some input parameters
* Discusses how to do "if" statements in a Declarative pipeline
* an input parameter called REFRESH_JOB which allows you to reload the Jenkinsfile to reload the parameters 
  from the Jenkinsfile without running the whole job.
* A way of using Bitbucket's "WebHook" to trigger a Jenkins job.

  
```

pipeline {
    // This is a DECLARATIVE pipeline
    // https://www.jenkins.io/doc/book/pipeline/syntax/

    agent any

    parameters {
        string(name: 'REPO',
               description: 'The Repository to clone.',
               defaultValue: 'ssh://git@git/andywis/mycode.git')

        string(name: 'BRANCH',
               description: 'The Branch to checkout.',
               defaultValue: 'jenkinsfile-for-automated-testing-TICKET-1789')

        booleanParam(name: 'REFRESH_JOB',
                    defaultValue: false,
                    description: '(No-Op) Re-Read Jenkinsfile and exit.')
    }

    triggers {
        /* this is an example of how to trigger a Jenkinsfile from a Bitbucket
         *  event using a "WebHook".
         * I was interested in triggering commits to a pull request.
         *
         * The WebHook does allow you to detect when a Pull request is created, 
         * and when a comment is added to a pull request, however Bitbucket 
         * does not have a built-in mechamism for detecting commits to an
         * already-open Pull request. As a simple work around, we can search 
         * for a specific string in a pull request comment, which will trigger
         * the test. In this case, the pull request comment must be exactly
         * "RE-TEST"
         *
         * For a new pull request, $.eventKey == "pr:opened"
         * For a comment change, $.eventKey == "pr:comment:added",
         *
         * The Bitbucket "detect commit" issue is discussed here:
         * https://community.atlassian.com/t5/Bitbucket-questions/Change-pull-request-refs-after-Commit-instead-of-after-Approval/qaq-p/194702
         * and here:
         * https://community.atlassian.com/t5/Bitbucket-questions/How-to-trigger-a-webhook-when-a-commit-is-pushed-to-an-open-pull/qaq-p/1029556
         *
         * I subsequently discovered a Bitbucket plugin called "Parameterized
         * Builds For Jenkins" which appears to detect subsequent commits to
         * a pull request as well as pull request creation. 
         * https://marketplace.atlassian.com/apps/1213179/parameterized-builds-for-jenkins?hosting=server&tab=overview
         * This will be a topic for a future example.
        */
        GenericTrigger(
            genericVariables: [
                [key: 'REF', value: '$'],

                // for a new pull request, $REF contains "eventKey":"pr:opened"
                // for a comment change, $REF contains "eventKey": "pr:comment:added",
                [key: 'PR_STATE', value: '$.pullRequest.state'],
                [key: 'PR_EVENT', value: '$.eventKey'],

                // will be an empty string if this is a new pull request
                [key: 'PR_COMMENT', value: '$.comment.text'],
                [key: 'BRANCH', value: '$.pullRequest.fromRef.displayId']
            ],
            token: 'zandywis1',
            causeString: 'Generic Cause',

            regexpFilterText: '$PR_STATE',
            regexpFilterExpression: 'OPEN'
        )
    }

    stages {
        stage('Prepare') {
            steps {
                // a "script" executes a block of "scripted pipeline" within the declarative pipeline.
                // this allows you to use if/else and try/catch blocks.
                // just about any Groovy (http://groovy-lang.org/syntax.html) can be used
                script {
                    sh '''echo branch=$BRANCH'''
                }

                // you can have as many script calls in a "steps" as you like
                // here we demonstrate the shell echo and the Groovy echo commands
                script {
                    sh '''echo This is an echo via a shell command '''
                    echo "This is a Jenkinsfile Echo"
                    print("This is a Jenkinsfile print command")  // print appears to be a synonym for echo

                    // different ways of printing a variable.
                    // N.B. I've seen parameters.REFRESH_JOB in some online docs; this doesn't work.
                    echo "The value of the parameter 'REFRESH_JOB' is... (printed twice)")
                    print("${REFRESH_JOB}")  
                    echo REFRESH_JOB
                }
                
                /* 
                * Work out if the bitbucket event should trigger the tests.
                */
                script {
                    if ("$PR_EVENT" == "pr:opened") {
                        env.RUN_THE_TEST = true
                        echo "Pull request was opened. The test should be run"
                    }
                    else if ("$PR_EVENT" == "pr:comment:added" && "$PR_COMMENT" == "RE-TEST") {
                        env.RUN_THE_TEST = true
                        echo "A comment was added which should trigger the test to run"
                    }
                    else {
                        env.RUN_THE_TEST = false
                        echo "Do not run the test"
                    }
                }



                /*
                 * This script demonstrates how to terminate the job early if REFRESH_JOB
                 * was ticked.
                 * It provides 2 approaches:
                 *   - one calls error() to terminate the job
                 *   - the other sets env.CONTINUE, which then needs a "when" expression
                 *     on all subsequent stages
                 *   - you don't need to implement both.
                */
                script {
                    // When testing a boolean tickbox, the following syntax
                    // works, but beware  
                    //       if (REFRESH_JOB == true)
                    // and
                    //       if (REFRESH_JOB)
                    // does not.
                    //
                    if ("${REFRESH_JOB}" == "true") {
                        env.CONTINUE = false
                        echo "REFRESH_JOB was ticked. Job parameters have been reloaded. Terminating..."
                        error("Job reloaded. Terminating job early.")
                        /* terminates with "failure" (because doing so with "pass" is much harder. )
                         * to terminate with success is harder; it appears the best practice way
                         * to accomplish this is to add a 'When' expression to every subsequent stage, 
                         * e.g.
                         *    when {expression { ${REFRESH_JOB}" == "true" }}
                        */
                    }
                }
            }
        }


        stage('Show inputs') {
            // even though CONTINUE is an env var, set above, this only seems to work if we cast it to a string
            when {expression { "${CONTINUE}" == "true" }}
            steps {
                script {
                    sh '''
                      echo Git trigger for  integration Testing.
                      echo PULL_REQUEST_STATE: $PR_STATE
                      echo PULL_REQUEST_EVENT: $PR_EVENT
        
                      echo PR Comment text '$PRCOMMENT' "
                    '''
                }
            }
        }


        stage('INT Test') {
            when {expression { "${CONTINUE}" == "true" }}
            steps {
                script {
                    sh "echo This step is to run the integration test."
                }
            }
        }
    }
}

```
