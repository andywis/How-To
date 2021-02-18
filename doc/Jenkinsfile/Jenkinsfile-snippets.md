# Jenkinsfile / Groovy snippets

(Dec 2020)

## Test that a variable exists
In this example we use a try/catch to handle the situation where a 
variable is not defined. `PR_URL` may or may not exist in this scenario...
```
stages {
    stage('Prepare') {
        steps {
            script {      
                try {
                    if ("$PRURL" == "") {
                        echo "PRURL is empty "
                        // error("Job terminated. PRURL not set.")
                    }
                } catch (e) {
                    echo "PR_URL is not defined"
                }
            }
        }
    }
}
```

## Terminating the job with an error
```
        ...
            script {
                if ("$some_condition" == "wrong condition") {
                    error("Job terminated. Something was bad.")
                }
            }     
```