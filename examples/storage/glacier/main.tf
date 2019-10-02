# Create s3 glacier vault
resource "aws_glacier_vault" "my_archive" {
  name = "nuke-glacier"
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-glacier"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

