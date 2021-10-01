# Get all availability zones
data "aws_availability_zones" "available" {
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "nuke" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}

resource "aws_ami_from_instance" "nuke" {
  name               = "ami-to-nuke"
  source_instance_id = aws_instance.nuke.id
}


### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-ami"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = "key_pair"
  older_than                     = "0d"
}
