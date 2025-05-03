# Deploy two lambda for testing with awspec

module "nuke-everything" {
  source                         = "../.."
  name                           = "nuke-everything"
  cloudwatch_schedule_expression = "cron(0 6 ? * * *)"
  older_than                     = "0d"
}
