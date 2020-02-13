#!/bin/bash

# Install the Latest version of Terraform
sudo pip install ansible
sudo ansible-galaxy install diodonfrost.terraform && sudo ln -s ~/.ansible/roles/diodonfrost.terraform ~/.ansible/roles/ansible-role-terraform
sudo ansible-pull -U https://github.com/diodonfrost/ansible-role-terraform tests/test.yml -e "terraform_version=${terraform_version}"
terraform -version
terraform init

# Test Terraform syntax
terraform validate \
  -var "region=${AWS_REGION}" \
  -var "name=nuke-all" \
  -var "cloudwatch_schedule_expression=cron(0 4 ? * MON-FRI *)" \
  -var "exclude_resources=glacier,eip,rds" \
  -var "older_than=14d"

# Terraform lint
terraform fmt -check -diff main.tf

# Test Terraform fixture example
cd examples/test_fixture || exist
terraform init
terraform validate
terraform fmt
terraform -v
