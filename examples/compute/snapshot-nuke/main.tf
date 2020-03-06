data "aws_availability_zones" "available" {}

resource "aws_ebs_volume" "nuke" {
  availability_zone = data.aws_availability_zones.available.names[0]
  size              = 20
}

resource "aws_ebs_snapshot" "nuke" {
  volume_id = aws_ebs_volume.nuke.id
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-snapshot"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = "key_pair"
  older_than                     = "0d"
}
