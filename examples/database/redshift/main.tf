# Get aws availability zones
data "aws_availability_zones" "available" {
}

resource "aws_vpc" "main" {
  cidr_block = "10.103.0.0/16"
}

resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.103.98.0/24"
}

resource "aws_subnet" "secondary" {
  availability_zone = data.aws_availability_zones.available.names[1]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.103.99.0/24"
}

# Create redshift subnet
resource "aws_redshift_subnet_group" "subnet_nuke" {
  name       = "redshift-subnet-nuke"
  subnet_ids = [aws_subnet.primary.id, aws_subnet.secondary.id]
}

# Create redshift param group
resource "aws_redshift_parameter_group" "param_nuke" {
  name   = "redshift-parameter-group-nuke"
  family = "redshift-1.0"

  parameter {
    name  = "require_ssl"
    value = "true"
  }

  parameter {
    name  = "query_group"
    value = "example"
  }

  parameter {
    name  = "enable_user_activity_logging"
    value = "true"
  }
}

# Create redshift cluster
resource "aws_redshift_cluster" "cluster_nuke" {
  cluster_identifier = "redshift-cluster-nuke"
  database_name      = "nuke"
  master_username    = "foo"
  master_password    = "Mustbe8characters"
  node_type          = "dc2.large"
  cluster_type       = "single-node"
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-redshift"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
