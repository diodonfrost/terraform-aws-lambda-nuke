# Get all availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Create rds aurora cluster
resource "aws_rds_cluster" "aurora_nuke" {
  cluster_identifier  = "aurora-cluster-nuke"
  availability_zones  = data.aws_availability_zones.available.names
  database_name       = "auroranuke"
  master_username     = "foo"
  master_password     = "barbut8chars"
  skip_final_snapshot = "true"
}

resource "aws_rds_cluster_instance" "aurora_nuke" {
  identifier         = "aurora-instance-nuke"
  cluster_identifier = aws_rds_cluster.aurora_nuke.id
  instance_class     = "db.t2.small"
}

# Create rds mariadb instance with tag
resource "aws_db_instance" "mariadb_nuke" {
  identifier          = "mariadb-instance-nuke"
  name                = "mariadbnuke"
  allocated_storage   = 10
  storage_type        = "gp2"
  engine              = "mariadb"
  engine_version      = "10.3"
  instance_class      = "db.t2.micro"
  username            = "foo"
  password            = "foobarbaz"
  skip_final_snapshot = "true"
}

# Create rds mysql instance with tag
resource "aws_db_instance" "mysql_nuke" {
  identifier          = "mysql-instance-nuke"
  name                = "mysqlnuke"
  allocated_storage   = 10
  storage_type        = "gp2"
  engine              = "mysql"
  engine_version      = "5.6"
  instance_class      = "db.t2.micro"
  username            = "foo"
  password            = "foobarbaz"
  skip_final_snapshot = "true"
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-rds"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

