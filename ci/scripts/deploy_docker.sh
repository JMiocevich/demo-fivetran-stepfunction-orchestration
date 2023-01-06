
cd src/ecs


echo "Logging into ECR"

aws ecr get-login-password \
    --region ap-southeast-2 \
| docker login \
    --username AWS \
    --password-stdin ${ACCOUNT_ID}.dkr.ecr.ap-southeast-2.amazonaws.com/${ecrRepo}



echo "Building Docker Image"
{
docker buildx build --platform linux/amd64 -t "${ACCOUNT_ID}".dkr.ecr.ap-southeast-2.amazonaws.com/${ecrRepo}:${ecrDockerImageName} .
} || {
  echo "## [Error]  Building Docker Image"
  exit -1
}



echo "Pushing Docker Image to ECR"
docker push "${ACCOUNT_ID}".dkr.ecr.ap-southeast-2.amazonaws.com/${ecrRepo}:${ecrDockerImageName}
} || {
  echo "## [Error] deploying docker image"
  exit -1
}