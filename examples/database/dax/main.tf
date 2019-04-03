resource "aws_iam_role" "dax_nuke" {
  name = "role-dax-nuke"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "dax.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = {
    tag-key = "tag-value"
  }
}

resource "aws_vpc" "main" {
  cidr_block = "10.99.0.0/16"
}

resource "aws_subnet" "primary" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.99.98.0/24"
}

resource "aws_subnet" "secondary" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.99.99.0/24"
}

# Creare dax subnet
resource "aws_dax_subnet_group" "dax_nuke" {
  name       = "dax-nuke"
  subnet_ids = ["${aws_subnet.primary.id}", "${aws_subnet.secondary.id}"]
}

# Create dax cluster
resource "aws_dax_cluster" "dax_nuke" {
  cluster_name       = "cluster-dax-nuke"
  iam_role_arn       = "${aws_iam_role.dax_nuke.arn}"
  node_type          = "dax.t2.small"
  replication_factor = 1
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "diodonfrost/lambda-nuke/aws"
  name                           = "nuke-dax"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
