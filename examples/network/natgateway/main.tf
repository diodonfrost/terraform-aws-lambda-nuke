# Create vpc
resource "aws_vpc" "main" {
  cidr_block = "10.121.0.0/16"
}

resource "aws_subnet" "primary" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.121.98.0/24"
}

# Create internet gateway
resource "aws_internet_gateway" "nuke_nat" {
  vpc_id = "${aws_vpc.main.id}"
}

# Create elastic ip for nat gateway
resource "aws_eip" "nuke_eip" {
  vpc = true
}

# Create nat gateway
resource "aws_nat_gateway" "nuke_nat" {
  allocation_id = "${aws_eip.nuke_eip.id}"
  subnet_id     = "${aws_subnet.primary.id}"
  depends_on    = ["aws_internet_gateway.nuke_nat"]
}


### Terraform modules ###

module "nuke-everything" {
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke-natgateway"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
