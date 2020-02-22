# Create vpc
resource "aws_vpc" "main" {
  cidr_block = "10.110.0.0/16"
}

# Create security group
resource "aws_security_group" "nuke_1" {
  name        = "sg_nuke_1"
  description = "sg nuke 1"
}

resource "aws_security_group" "nuke_2" {
  name        = "sg_nuke_2"
  description = "sg nuke 2"
}

resource "aws_security_group_rule" "nuke_ingress_1" {
  type      = "ingress"
  from_port = 443
  to_port   = 443
  protocol  = "tcp"

  source_security_group_id = aws_security_group.nuke_2.id
  security_group_id        = aws_security_group.nuke_1.id
}

resource "aws_security_group_rule" "nuke_ingress_2" {
  type      = "ingress"
  from_port = 443
  to_port   = 443
  protocol  = "tcp"

  source_security_group_id = aws_security_group.nuke_1.id
  security_group_id        = aws_security_group.nuke_2.id
}

resource "aws_security_group_rule" "nuke_ingress_http_1" {
  type      = "ingress"
  from_port = 80
  to_port   = 80
  protocol  = "tcp"

  source_security_group_id = aws_security_group.nuke_2.id
  security_group_id        = aws_security_group.nuke_1.id
}

resource "aws_security_group_rule" "nuke_ingress_http_2" {
  type      = "ingress"
  from_port = 80
  to_port   = 80
  protocol  = "tcp"

  source_security_group_id = aws_security_group.nuke_1.id
  security_group_id        = aws_security_group.nuke_2.id
}

resource "aws_security_group_rule" "nuke_egress_https_1" {
  type      = "egress"
  from_port = 443
  to_port   = 443
  protocol  = "tcp"

  source_security_group_id = aws_security_group.nuke_2.id
  security_group_id        = aws_security_group.nuke_1.id
}

resource "aws_security_group_rule" "nuke_egress_https_2" {
  type      = "egress"
  from_port = 443
  to_port   = 443
  protocol  = "tcp"

  source_security_group_id = aws_security_group.nuke_1.id
  security_group_id        = aws_security_group.nuke_2.id
}

resource "aws_security_group_rule" "nuke_egress_http_1" {
  type      = "egress"
  from_port = 80
  to_port   = 80
  protocol  = "tcp"

  source_security_group_id = aws_security_group.nuke_2.id
  security_group_id        = aws_security_group.nuke_1.id
}

resource "aws_security_group_rule" "nuke_egress_http_2" {
  type      = "egress"
  from_port = 80
  to_port   = 80
  protocol  = "tcp"

  source_security_group_id = aws_security_group.nuke_1.id
  security_group_id        = aws_security_group.nuke_2.id
}


### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-security-group"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

