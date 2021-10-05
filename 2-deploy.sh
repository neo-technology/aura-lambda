#!/bin/bash
set -eo pipefail
ARTIFACT_BUCKET=$(cat bucket-name.txt)

##############################
# Set your Aura values here!
##############################
. .env

aws cloudformation package --template-file template.yml --s3-bucket $ARTIFACT_BUCKET --output-template-file out.yml
aws cloudformation deploy --template-file out.yml --stack-name aura-lambda --capabilities CAPABILITY_NAMED_IAM

FUNCTION=$(aws cloudformation describe-stack-resource --stack-name aura-lambda --logical-resource-id function --query 'StackResourceDetail.PhysicalResourceId' --output text)

# Plug environment variables into AWS Lambda execution context 
aws lambda update-function-configuration --function-name $FUNCTION \
    --environment "Variables={NEO4J_USERNAME=$NEO4J_USERNAME,NEO4J_PASSWORD=$NEO4J_PASSWORD,NEO4J_URI=$NEO4J_URI}"