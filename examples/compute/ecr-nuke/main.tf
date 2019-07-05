# Create EC2 Container Registry Repository
resource "aws_ecr_repository" "nuke" {
  name = "nuke-ecr"
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-ecr"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
