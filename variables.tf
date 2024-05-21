# Terraform variables file

# Set cloudwatch events for shutingdown instances
# trigger lambda functuon every night at 22h00 from Monday to Friday
# cf doc : https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
variable "cloudwatch_schedule_expression" {
  description = "Define the aws cloudwatch event rule schedule expression"
  type        = string
  default     = "cron(0 22 ? * MON-FRI *)"
}

variable "name" {
  description = "Define name to use for lambda function, cloudwatch event and iam role"
  type        = string
  default     = "everything"
}

variable "custom_iam_role_arn" {
  description = "Custom IAM role arn for the scheduling lambda"
  type        = string
  default     = null
}

variable "kms_key_arn" {
  description = "The ARN for the KMS encryption key. If this configuration is not provided when environment variables are in use, AWS Lambda uses a default service key."
  type        = string
  default     = null
}

variable "aws_regions" {
  description = "A list of one or more aws regions where the lambda will be apply, default use the current region"
  type        = list(string)
  default     = null
}

variable "exclude_resources" {
  description = "Define the resources that will not be destroyed"
  type        = string
  default     = null
}

variable "older_than" {
  description = "Only destroy resources that were created before a certain period"
  type        = string
  default     = "0d"
}

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(any)
  default     = null
}

variable "TARGET_RESOURCE" {
  description = "Define the specific resources that will be destroyed"
  type        = string
  default     = null
}
