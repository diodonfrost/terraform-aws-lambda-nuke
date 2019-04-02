
# Create ECS cluster
resource "aws_ecs_cluster" "nuke" {
  name = "nuke-ecs"
}


### Terraform modules ###

module "nuke-everything" {
  source                         = "../../.."
  name                           = "nuke-eks"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
