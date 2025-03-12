#!/bin/bash
cd docker

export AWS_ACCOUNT=$(aws sts get-caller-identity --profile miso --query Account --output text)
export ECR_REPO=$AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Construir ventas
docker build --platform linux/amd64 -t ventas \
  --file Dockerfile.ventas \
  ../src/ventas

docker tag ventas:latest $ECR_REPO/ventas:latest

docker push $ECR_REPO/ventas:latest