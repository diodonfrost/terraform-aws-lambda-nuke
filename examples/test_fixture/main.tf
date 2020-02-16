# Deploy two lambda for testing with awspec

resource "aws_kms_key" "scheduler" {
  description             = "test kms option on scheduler module"
  deletion_window_in_days = 7
}

module "nuke-everything" {
  source                         = "../.."
  name                           = "nuke-everything" 
  kms_key_arn                    = aws_kms_key.scheduler.arn
  cloudwatch_schedule_expression = "cron(0 22 ? * MON-FRI *)"
  older_than                     = "0d"
}

module "nuke-except-rds" {
  source                         = "../.."
  name                           = "nuke-except-rds" 
  cloudwatch_schedule_expression = "cron(0 22 ? * MON-FRI *)"
  older_than                     = "0d"
}
