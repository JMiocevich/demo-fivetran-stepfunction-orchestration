
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export stackName="fivetran-orchestration"

export ecrRepo="${stackName}-ecr"
export ecrDockerImageName="${stackName}-docker-image"
export deploymentBucketStackName="${stackName}-deployment-stack"
export deploymentBucketName="${deploymentBucketStackName}-deployment-bucket"



echo "Sam Build"
./ci/scripts/build.sh


echo "Deploying"
./ci/scripts/deploy.sh


echo "Docker to ECR"
./ci/scripts/deploy_docker.sh



