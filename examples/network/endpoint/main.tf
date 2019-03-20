
# Get current region
data "aws_region" "current" {}

# Create vpc
resource "aws_vpc" "main" {
  cidr_block = "10.110.0.0/16"
}

# Create s3 endpoint
resource "aws_vpc_endpoint" "nuke_s3_endpoint" {
  vpc_id       = "${aws_vpc.main.id}"
  service_name = "com.amazonaws.${data.aws_region.current.name}.s3"
}

# Create dynamodb endpoint
resource "aws_vpc_endpoint" "nuke_dynamodb_endpoint" {
  vpc_id       = "${aws_vpc.main.id}"
  service_name = "com.amazonaws.${data.aws_region.current.name}.dynamodb"
}


### Terraform modules ###

module "nuke-everything" {
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke-endpoint"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
