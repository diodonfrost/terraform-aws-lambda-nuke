# terraform-aws-lambda-nuke
Terraform module which create lambda which nuke all resources on aws account

## Features

*   Aws lambda runtine Python 3.6
*   Compute resources nuke:
    -   Ec2 Instances
    -   Launch Templates
    -   Ebs Volumes
    -   Ebs Life Cycle Manager
    -   Load Balancers
    -   Target Groups
    -   Launch Configurations
    -   Auto Scaling Groups
    -   Target Groups
    -   Key Pairs
    -   Placement Groups
    -   Elastic Container Registry
    -   Elastic Container Clusters
    -   Elastic Kubernetes Services


## Usage
```hcl
module "nuke_everything_older_than_7d" {
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke_everything"
  cloudwatch_schedule_expression = "cron(0 00 ? * FRI *)"
  exclude_resources              = "key_pairs,rds"
  older_than                     = "7d"
}
```

## Examples

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| name | Define name to use for lambda function, cloudwatch event and iam role | string | n/a | yes |
| cloudwatch_schedule_expression | The scheduling expression | string | `"cron(0 22 ? * MON-FRI *)"` | yes |
| exclude_resources | Define the resources that will be not destroyed | string |  | no |
| older_than | Only destroy resources that were created before a certain period | string | 0d | no |

## Outputs

| Name | Description |
|------|-------------|
| lambda_iam_role_arn | The Amazon Resource Name (ARN) identifying your Lambda Function |
| lambda_iam_role_name | The name of the IAM role used by Lambda function |
| nuke_lambda_arn | The ARN of the Lambda function |
| nuke_function_name | The name of the Lambda function |
| nuke_lambda_invoke_arn | The ARN to be used for invoking Lambda function from API Gateway |
| nuke_lambda_function_last_modified | The date Lambda function was last modified |
| nuke_lambda_function_version | Latest published version of your Lambda function |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Tests

This module has been packaged with [awspec](https://github.com/k1LoW/awspec) tests through test kitchen. To run them:

Install kitchen-terraform and awspec:

```shell
# Install dependencies
gem install bundler
bundle install
```

Launch kitchen tests:

```shell
# List all tests with kitchen
kitchen list

# Build, and tests terraform module
kitchen test lambda-scheduler-aws

# for development, create environment
kitchen converge lambda-scheduler-aws

# Apply awspec tests
kitchen verify lambda-scheduler-aws
```

## Authors

Modules managed by [diodonfrost](https://github.com/diodonfrost)

## Licence

Apache 2 Licensed. See LICENSE for full details.

## Resources

*   [cloudwatch schedule expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
*   [Python boto3 ec2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
*   [Python boto3 rds](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html)
*   [Python boto3 autoscaling](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html)
