provider "aws" {
  region = "eu-west-3"
}

# Deploy two lambda for testing with awspec

module "nuke-everything" {
  source                         = "../.."
  name                           = "nuke-everything"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
