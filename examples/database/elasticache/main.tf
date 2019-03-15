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
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke-elasticache"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
