# Create vpc
resource "aws_vpc" "main" {
  cidr_block = "10.110.0.0/16"
}

# Create security group
resource "aws_security_group" "nuke_security_group" {
  name        = "allow_tls_nuke"
  description = "Allow TLS inbound traffic"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["192.168.1.1/32"]
  }
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-security-group"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

