# Create s3 glacier vault
resource "aws_glacier_vault" "my_archive" {
  name = "nuke-glacier"
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke-s3"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
