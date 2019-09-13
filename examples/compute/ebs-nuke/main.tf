# Get all availability zones
data "aws_availability_zones" "available" {
}

# Create ebs volume
resource "aws_ebs_volume" "nuke" {
  count             = 3
  availability_zone = data.aws_availability_zones.available.names[0]
  size              = 20
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-ebs"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = "key_pair"
  older_than                     = "0d"
}

