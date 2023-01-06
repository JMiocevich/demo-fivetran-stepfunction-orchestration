

{
  aws cloudformation deploy \
    --stack-name ${deploymentBucketStackName} \
    --template-file infrastructure/deployment-bucket.yml \
    --parameter-overrides DeploymentBucketName="${deploymentBucketName}"  \
    --capabilities CAPABILITY_IAM \
    --no-fail-on-empty-changeset
} || {
  echo "## [Error] deploying S3 Bucket for Deployment Artifacts"
  exit -1
}



{
sam deploy \
    --stack-name ${stackName} \
    --parameter-overrides \
        ecrRepo=${ecrRepo} \
        ecrDockerImageName=${ecrDockerImageName} \
    --s3-bucket ${deploymentBucketName} \
    --s3-prefix ${stackName} \
    --region "ap-southeast-2" \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
    --no-fail-on-empty-changeset \
    --no-confirm-changeset 
} || {
  echo "## [Error] deploying Cloudformation Stack"
  exit -1
}