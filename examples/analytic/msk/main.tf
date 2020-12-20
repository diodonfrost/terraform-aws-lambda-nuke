resource "aws_vpc" "kafka" {
  cidr_block = "192.168.0.0/22"
}

data "aws_availability_zones" "kafka" {
  state = "available"
}

resource "aws_subnet" "az1" {
  availability_zone = data.aws_availability_zones.kafka.names[0]
  cidr_block        = "192.168.0.0/24"
  vpc_id            = aws_vpc.kafka.id
}

resource "aws_subnet" "az2" {
  availability_zone = data.aws_availability_zones.kafka.names[1]
  cidr_block        = "192.168.1.0/24"
  vpc_id            = aws_vpc.kafka.id
}

resource "aws_subnet" "az3" {
  availability_zone = data.aws_availability_zones.kafka.names[2]
  cidr_block        = "192.168.2.0/24"
  vpc_id            = aws_vpc.kafka.id
}

resource "aws_security_group" "kafka" {
  vpc_id = aws_vpc.kafka.id
}

resource "aws_kms_key" "kafka" {
  description = "kafka test nuke"
}

resource "aws_msk_cluster" "nuke" {
  cluster_name           = "kafka-nuke"
  kafka_version          = "2.3.1"
  number_of_broker_nodes = 3

  broker_node_group_info {
    instance_type   = "kafka.m5.large"
    ebs_volume_size = 1000
    client_subnets = [
      aws_subnet.az1.id,
      aws_subnet.az2.id,
      aws_subnet.az3.id,
    ]
    security_groups = [aws_security_group.kafka.id]
  }

  encryption_info {
    encryption_at_rest_kms_key_arn = aws_kms_key.kafka.arn

    encryption_in_transit {
      client_broker = "TLS"
      in_cluster    = true
    }
  }

  open_monitoring {
    prometheus {
      jmx_exporter {
        enabled_in_broker = true
      }
      node_exporter {
        enabled_in_broker = true
      }
    }
  }
}


### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-msk"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = "key_pair"
  older_than                     = "0d"
}
