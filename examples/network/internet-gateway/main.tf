# Create vpc
resource "aws_vpc" "main" {
  cidr_block = "10.124.0.0/16"
}

resource "aws_subnet" "primary" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.124.98.0/24"
}

# Create internet gateway
resource "aws_internet_gateway" "nuke_internet_gateway" {
  vpc_id = "${aws_vpc.main.id}"
}

# Create egress internet gateway
resource "aws_egress_only_internet_gateway" "nuke_internet_gateway" {
  vpc_id = "${aws_vpc.main.id}"
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke-internet-gateway"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
