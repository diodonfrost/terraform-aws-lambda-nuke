# Create ebs volume
resource "aws_ebs_volume" "nuke" {
  count             = 3
  availability_zone = "eu-west-3a"
  size              = 20
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke-ebs"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
