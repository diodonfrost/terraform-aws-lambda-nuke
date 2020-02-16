# terraform-aws-lambda-nuke

[![Build Status](https://api.travis-ci.com/diodonfrost/terraform-aws-lambda-nuke.svg?branch=master)](https://travis-ci.com/diodonfrost/terraform-aws-lambda-nuke)


Terraform module which create lambda which nuke all resources on aws account

## Requirements

This role was developed using python lib boto3 1.9.46 Backwards compatibility is not guaranteed.

## Terraform versions

For Terraform 0.12 use version v2.* of this module.

If you are using Terraform 0.11 you can use versions v1.*.

## Caveats
This following resources are not supported because creation timestamp are not present:

*   Compute
    -   ecs
*   Database:
    -   dax

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

*   [Compute-nuke](https://github.com/diodonfrost/terraform-aws-lambda-nuke/tree/master/examples/compute) Create lambda function to nuke compute resources on Friday at 23:00 Gmt

*   [Storage-nuke](https://github.com/diodonfrost/terraform-aws-lambda-nuke/tree/master/examples/storage) Create lambda function to nuke storage resources on Friday at 23:00 Gmt

*   [test fixture](https://github.com/diodonfrost/terraform-aws-lambda-lambda/tree/master/examples/test_fixture) - Deploy environment for testing module with kitchen-ci and awspec

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| name | Define name to use for lambda function, cloudwatch event and iam role | string | n/a | yes |
| custom_iam_role_arn | Custom IAM role arn for the scheduling lambda | string | null | no |
| kms_key_arn | The ARN for the KMS encryption key. If this configuration is not provided when environment variables are in use, AWS Lambda uses a default service key | string | null | no |
| aws_regions | A list of one or more aws regions where the lambda will be apply, default use the current region | list | null | no |
| cloudwatch_schedule_expression | The scheduling expression | string | `"cron(0 22 ? * MON-FRI *)"` | yes |
| exclude_resources | Define the resources that will be not destroyed | string | null | no |
| older_than | Only destroy resources that were created before a certain period | string | 0d | no |

## Outputs

| Name | Description |
|------|-------------|
| lambda_iam_role_arn | The ARN of the IAM role used by Lambda function |
| lambda_iam_role_name | The name of the IAM role used by Lambda function |
| nuke_lambda_arn | The ARN of the Lambda function |
| nuke_function_name | The name of the Lambda function |
| nuke_lambda_invoke_arn | The ARN to be used for invoking Lambda function from API Gateway |
| nuke_lambda_function_last_modified | The date Lambda function was last modified |
| nuke_lambda_function_version | Latest published version of your Lambda function |
| scheduler_log_group_name | The name of the scheduler log group |
| scheduler_log_group_arn | The Amazon Resource Name (ARN) specifying the log group |

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
kitchen test

# for development, create environment
kitchen converge

# Apply awspec tests
kitchen verify
```

## Authors

Modules managed by [diodonfrost](https://github.com/diodonfrost)

## Licence

Apache 2 Licensed. See LICENSE for full details.

## Resources

*   [cloudwatch schedule expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
*   [Python boto3 paginator](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html)
*   [Python boto3 ec2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
*   [Python boto3 rds](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html)
*   [Python boto3 autoscaling](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html)
