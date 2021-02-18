# Integrate Jenkins and Bitbucket

(Jan 2021)

Setting up Bitbucket to trigger a Jenkins job can be accomplished with the
[Bitbucket Plugin](https://plugins.jenkins.io/bitbucket/) for Jenkins.
A "Webhook" is added to your repository in Bitbucket that will trigger a
Jenkins job.

Once the build has completed, it is necessary to report back to Bitbucket
so that the pull request can state whether the build has passed or failed.

This is possible directly with the API, as we'll see below. Plugins such as the
[Bitbucket Server Notifier](https://plugins.jenkins.io/stashNotifier/) or the
[Bitbucket Build Status Notifier](https://plugins.jenkins.io/bitbucket-build-status-notifier/)
may be able to do this as well.


# Build a simple Jenkinsfile
First, we need a simple pipeline in Jenkins, and a little bit of config in our
repository.

In **Jenkins**, configure your job to use a **Generic Webhook Trigger** and
set the **Token**. We also give this token to Bitbucket. For example, let's set
it to "red_int_test"

In **Bitbucket**, add a WebHook with the URL from the 'token' section in the
Jenkins job e.g.
https://jenkins001.andywis.local/generic-webhook-trigger/invoke?token=red_int_test
(note it has the same token)
* set the webhook to trigger when a pull request is **opened**

Back in **Jenkins**, in the "Generic Webhook Trigger" section, add a set of
"Post content parameters":
* click "Add"
* Variable: BRANCH
* Expression: $.pullRequest.toRef.displayId
* Tick "JsonPath"
* leave Value Filter and Default Value blank
* Ensure there is a matching job parameter, further up in the job def (in this case,
  a param called "BRANCH")

Repeat the above for
* REPO = $.pullRequest.toRef.repository.links.clone[?(@.name == 'ssh')].href
* DESCRIPTION  = $.pullRequest.description
* TO_REF = $.pullRequest.toRef.latestCommit
* FROM_REF = $.pullRequest.fromRef.latestCommit

These Post Content parameters are needed to convert the JSON payload from the
webhook into Jenkins parameters. The parameters you need will depend on what
you need from the Jenkins job.

You can now trigger the Jenkins job by creating a pull request.

In order to develop the plugin, I also caused it to trigger when a comment
is added. This makes it a lot easier to re-run the job.


# Using the Bitbucket API to report Build status

To send build information back to Bitbucket, we'll use the REST API.
(links in Resources, below).

I attempted to write a Groovy function to make the HTTP Post request,
but could not get it to work, as the method calls I found in examples
were forbidden by the Groovy Sandbox. Instead, I opted for a simple
"curl" solution.

The Jenkinsfile function to post back to Bitbucket looks like this:


**Notes**
* In our environment, we have to use curl's -k option as well; please
don't, if you can set up your certificates to avoid doing so.
* You shouldn't need to adjust the payload, below. Be very careful with
the backslashes if you do!
* this function goes at the top of the script.
* Note, it does **not** need a @NonCPS annotation immediately before the
  function, because it's using 'sh'.
  see https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches/ .
```
//
// Use Curl to post to Bitbucket's Build Status API
def updateBuildStatus(bitbucketBaseUrl, user, password, commit_hash, state, key, name, buildUrl, description) {

    url = "$bitbucketBaseUrl/rest/build-status/1.0/commits/$commit_hash"
    creds = user + ":" + password
    payload = """{ \\"state\\": \\"$state\\", \\"key\\": \\"$key\\", \\"name\\": \\"$name\\", \\"url\\": \\"$buildUrl\\", \\"description\\": \\"$description\\" }"""

    sh """
        echo "    URL =      ${url}"
        echo "    PAYLOAD =  ${payload}"
        curl -u "${creds}" -H "Content-Type: application/json" -X POST "${url}" -d "${payload}"
    """
}
```
Once the above function is written, your Jenkinsfile stage can make use of it...

```
        stage('Report Back') {
            steps {
                withCredentials([
                    [$class: "UsernamePasswordMultiBinding", credentialsId: 'Jenkins-to-bitbucket',
                     usernameVariable: 'user', passwordVariable: 'password']
                ]) {
                    script {
                        bitbucketBaseUrl = "https://git.andywis.local"
                        commit_hash = FROM_REF  // see notes above
                        state = "FAILED"  // one of <INPROGRESS|SUCCESSFUL|FAILED>
                        key = "a_build_key"  // uniquely identifies this build
                        name = "name of your Jenkins job"
                        buildUrl = "${JOB_URL}${BUILD_NUMBER}"
                        description = "my test job"

                        updateBuildStatus(bitbucketBaseUrl, user, password, commit_hash, state, key, name, buildUrl, description)
                    }
                }
            }
        }
```
You may find
[this list of environment variables](https://e.printstacktrace.blog/jenkins-pipeline-environment-variables-the-definitive-guide/)
useful for populating the parameters. For example, key can be set to

```
    key = "${REPO}__${BRANCH}"
```

# Triggering the Build Status API after a Jenkinsfile failure
Obviously, you want your build status to appear in Bitbucket, indicating if
the job succeeded or failed. When the build fails, subsequent stages are
skipped, which mean you can't report back to Bitbucket.

However, a Jenkinsfile also supports a `post` section, which will execute
after the normal stages. (see [here](https://www.jenkins.io/doc/book/pipeline/syntax/#post))

In a regular stage, you can use environment variables to report the results
of an operation, e.g.

```javascript
        stage('INT Test') {    
            steps {
                script {
                    // here is a dummy "integration test"
                    env.INT_TEST_SUCCESS = false
                    sh "grep Zebedee /etc/hosts"   //    should fail.
                    env.INT_TEST_SUCCESS = true
                }
            }
        }
```
You can then add a `post` step to report back to Bitbucket, with knowledge
of whether your "INT Test" stage passed or not. The value of INT_TEST_SUCCESS
can be used to set "state" to the appropriate "SUCCESSFUL" or "FAILED"

"post" is at the same level of indent as "stages"
```javascript
        }  // closing brace of last "stage"
    }  // closing brace of "stages"
    post {
        always {
            withCredentials([ ... ]) {
                script {
                    echo "Was the INT Test successful? ${INT_TEST_SUCCESS}"
                    if (INT_TEST_SUCCESS == "true") {
                        state = "SUCCESSFUL"
                    }else{
                        state = "FAILED"
                    }
                    updateBuildStatus_curl( ... , state, ... )
                }
            }
        }
    }
}  // closing brace for "pipeline"
```

## Resources
[Atlassian How-to](https://developer.atlassian.com/server/bitbucket/how-tos/updating-build-status-for-commits/)

[Atlassian REST documentation](https://docs.atlassian.com/bitbucket-server/rest/7.8.1/bitbucket-build-rest.html)
