# Create EFS filesystem
resource "aws_efs_file_system" "nuke" {
  creation_token = "efs-nuke"
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-efs"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

