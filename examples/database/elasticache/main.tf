# Get aws availability zones
data "aws_availability_zones" "available" {
}

resource "aws_vpc" "main" {
  cidr_block = "10.96.0.0/16"
}

resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.96.98.0/24"
}

resource "aws_subnet" "secondary" {
  availability_zone = data.aws_availability_zones.available.names[1]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.96.99.0/24"
}

# Create elasticache subnet
resource "aws_elasticache_subnet_group" "nuke_subnet" {
  name       = "cache-subnet-nuke"
  subnet_ids = [aws_subnet.primary.id, aws_subnet.secondary.id]
}

# Create elasticache parameter group
resource "aws_elasticache_parameter_group" "nuke_param" {
  name   = "cache-params-nuke"
  family = "redis2.8"

  parameter {
    name  = "activerehashing"
    value = "yes"
  }

  parameter {
    name  = "min-slaves-to-write"
    value = "2"
  }
}

# Create memcached cluster
resource "aws_elasticache_cluster" "nuke_memcached" {
  cluster_id           = "memcached-nuke"
  engine               = "memcached"
  node_type            = "cache.t2.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.memcached1.5"
  engine_version       = "1.5.10"
  port                 = 11211
}

# Create redis cluster
resource "aws_elasticache_cluster" "nuke_redis" {
  cluster_id           = "redis-nuke"
  engine               = "redis"
  node_type            = "cache.t2.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis3.2"
  engine_version       = "3.2.10"
  port                 = 6379
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-elasticache"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

