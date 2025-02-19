#!/bin/bash
cd docker

export AWS_ACCOUNT=$(aws sts get-caller-identity --profile miso --query Account --output text)
export ECR_REPO=$AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Construir monitor
docker build --platform linux/amd64 -t monitor \
  --file Dockerfile.monitor \
  ../src/monitor

# Construir purchases
docker build --platform linux/amd64 -t purchases \
  --file Dockerfile.purchases \
  ../src/purchases

docker tag monitor:latest $ECR_REPO/monitor:latest
docker tag purchases:latest $ECR_REPO/purchases:latest

docker push $ECR_REPO/monitor:latest
docker push $ECR_REPO/purchases:latest