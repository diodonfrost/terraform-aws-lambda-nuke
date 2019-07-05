# Create S3 bucket
resource "aws_s3_bucket" "nuke" {
  bucket = "s3-nuke"
  acl    = "private"
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-s3"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
