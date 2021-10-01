# Get all availability zones
data "aws_availability_zones" "available" {
}

# Create vpc for elb
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Create subnets for elb
resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.10.0/24"
}

# Create subnets for elb
resource "aws_subnet" "secondary" {
  availability_zone = data.aws_availability_zones.available.names[1]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.20.0/24"
}

# Create application load balancer
resource "aws_lb" "app_nuke" {
  name               = "lb-app-nuke"
  internal           = true
  load_balancer_type = "application"
  subnets            = [aws_subnet.primary.id, aws_subnet.secondary.id]
}

# Create network load balancer
resource "aws_lb" "network_nuke" {
  name               = "lb-network-nuke"
  internal           = true
  load_balancer_type = "network"
  subnets            = [aws_subnet.primary.id, aws_subnet.secondary.id]
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-loadbalancer"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
