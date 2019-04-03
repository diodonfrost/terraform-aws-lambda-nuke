# Create vpc
resource "aws_vpc" "main" {
  cidr_block = "10.123.0.0/16"
}

resource "aws_subnet" "primary" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.123.98.0/24"
}

# Create internet gateway
resource "aws_internet_gateway" "main" {
  vpc_id = "${aws_vpc.main.id}"
}

# Create route table
resource "aws_route_table" "nuke_routetable" {
  vpc_id = "${aws_vpc.main.id}"

  route {
    cidr_block = "10.0.1.0/24"
    gateway_id = "${aws_internet_gateway.main.id}"
  }

  route {
    cidr_block = "10.0.2.0/24"
    gateway_id = "${aws_internet_gateway.main.id}"
  }
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke-routetable"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
