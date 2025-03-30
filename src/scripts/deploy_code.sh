#!/bin/bash

# Define variables
AWS_INSTANCE="your_aws_instance_address"
AWS_USER="your_aws_user"
REPO_URL="git@github.com:mandilshashank/stock-pred.git"
PROJECT_DIR="stock-pred"

# SSH into the AWS instance, create the project directory if it doesn't exist, and clone the repository
ssh $AWS_USER@$AWS_INSTANCE << EOF
  if [ ! -d "$PROJECT_DIR" ]; then
    mkdir -p $PROJECT_DIR
  fi
  git clone $REPO_URL $PROJECT_DIR
  cd $PROJECT_DIR
  bash install_dependencies.sh
EOF