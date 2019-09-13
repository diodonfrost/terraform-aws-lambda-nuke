# Deploy two lambda for testing with awspec

module "nuke-everything" {
  source                         = "../.."
  name                           = var.name
  cloudwatch_schedule_expression = var.cloudwatch_schedule_expression
  exclude_resources              = var.exclude_resources
  older_than                     = var.older_than
}

