# Create vpc
resource "aws_vpc" "main" {
  cidr_block = "10.122.0.0/16"
}

resource "aws_subnet" "primary" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.122.98.0/24"
}

# Create internet gateway
resource "aws_internet_gateway" "nuke_nat" {
  vpc_id = aws_vpc.main.id
}

# Create elastic ip
resource "aws_eip" "nuke_eip_one" {
  domain = "vpc"
}

# Create elastic ip
resource "aws_eip" "nuke_eip_two" {
  domain = "vpc"
}

# Create elastic ip
resource "aws_eip" "nuke_eip_three" {
  domain = "vpc"
}

### Terraform modules ###

module "nuke_everything" {
  source                         = "../../../"
  name                           = "nuke-eip"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
