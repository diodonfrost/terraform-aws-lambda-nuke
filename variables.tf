# Terraform variables file

# Set cloudwatch events for shutingdown instances
# trigger lambda functuon every night at 22h00 from Monday to Friday
# cf doc : https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
variable "cloudwatch_schedule_expression" {
  description = "Define the aws cloudwatch event rule schedule expression"
  default = "cron(0 22 ? * MON-FRI *)"
}

variable "name" {
  description = "Define name to use for lambda function, cloudwatch event and iam role"
  default     = "nuke"
}

variable "exclude_resources" {
  type        = "string"
  description = "Define the resources that will not be destroyed"
  default     = "key_pair"
}

variable "older_than" {
  description = "Only destroy resources that were created before a certain period"
  default     = "0d"
}
