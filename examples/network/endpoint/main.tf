# Get current region
data "aws_region" "current" {
}

# Get all availability zones
data "aws_availability_zones" "available" {
}

# Create vpc
resource "aws_vpc" "main" {
  cidr_block = "10.120.0.0/16"
}

resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.120.98.0/24"
}

resource "aws_subnet" "secondary" {
  availability_zone = data.aws_availability_zones.available.names[1]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.120.99.0/24"
}

# Create a loadbalancer
resource "aws_lb" "nuke_lb" {
  name               = "lb-nuke"
  load_balancer_type = "network"
  internal           = true
  subnets            = [aws_subnet.primary.id, aws_subnet.secondary.id]
}

# Create s3 endpoint
resource "aws_vpc_endpoint" "nuke_s3_endpoint" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${data.aws_region.current.name}.s3"
}

# Create dynamodb endpoint
resource "aws_vpc_endpoint" "nuke_dynamodb_endpoint" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${data.aws_region.current.name}.dynamodb"
}

# Create load balancer endpoint
resource "aws_vpc_endpoint_service" "nuke_loadbalancer_endpoint" {
  acceptance_required        = false
  network_load_balancer_arns = [aws_lb.nuke_lb.arn]
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-endpoint"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
