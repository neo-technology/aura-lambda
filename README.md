## Steps

### Set up your Python virtual environment

`python3 -m venv venv`

### Create an AWS S3 bucket to hold artifacts you're deploying to Lambda

This step requires that you have an authenticated aws client in place that can run the `aws` command.

`./0-create-bucket.sh`

The output of this is a file called `bucket-name.txt` which will contain a temporary bucket where deploy artifacts are staged.

### Install Python Modules

`./1-build.layer.sh`

### Deploy your Lambda

Create a file called `.env` in the root directory with this content, substituting your Neo4j Aura values:

```
export NEO4J_PASSWORD=mySecretPassword
export NEO4J_URI=neo4j+s://dbid.databases.neo4j.io
export NEO4J_USERNAME=neo4j
```

That file must be created for the deploy to work, as these environment variables will be provided to the
lambda.

Next, deploy the lambda like so:

`./2-deploy.sh`

Sample output:

```
$ ./2-deploy.sh 
Uploading to 3d20b9c7d47cbd54fea7edc2309757d1  11228394 / 11228394.0  (100.00%)
Successfully packaged artifacts and wrote output template to file out.yml.
Execute the following command to deploy the packaged template
aws cloudformation deploy --template-file /Users/username/aura-lambda/out.yml --stack-name <YOUR STACK NAME>

Waiting for changeset to be created..
Waiting for stack create/update to complete
Successfully created/updated stack - aura-lambda
```

### Invoke the Function

`./3-invoke.sh`

This will in a loop, every 2 seconds, submit the sample event (`event.json`) to the lambda function.

If all goes well, you will start to see records appear in your Neo4j Aura instance!

### Cleanup

When you're finished, to delete all resources associated with this sample function:

`./4-cleanup.sh`
