# Get aws availability zones
data "aws_availability_zones" "available" {
}

resource "aws_vpc" "main" {
  cidr_block = "10.102.0.0/16"
}

resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.102.98.0/24"
}

resource "aws_subnet" "secondary" {
  availability_zone = data.aws_availability_zones.available.names[1]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.102.99.0/24"
}

# Create neptune subnet
resource "aws_neptune_subnet_group" "subnet_nuke" {
  name       = "netpune-subnet-nuke"
  subnet_ids = [aws_subnet.primary.id, aws_subnet.secondary.id]
}

# Create neptune params group
resource "aws_neptune_cluster_parameter_group" "param_nuke" {
  family      = "neptune1"
  name        = "neptune-param-nuke"
  description = "neptune cluster parameter group"

  parameter {
    name  = "neptune_enable_audit_log"
    value = 1
  }
}

# Create neptune cluster
resource "aws_neptune_cluster" "cluster_nuke" {
  cluster_identifier                  = "neptune-cluster-nuke"
  engine                              = "neptune"
  backup_retention_period             = 1
  preferred_backup_window             = "07:00-09:00"
  skip_final_snapshot                 = true
  iam_database_authentication_enabled = true
  apply_immediately                   = true
}

# Create neptune instance
resource "aws_neptune_cluster_instance" "instance_nuke" {
  cluster_identifier = aws_neptune_cluster.cluster_nuke.id
  engine             = "neptune"
  instance_class     = "db.r4.large"
  apply_immediately  = true
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-neptune"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

