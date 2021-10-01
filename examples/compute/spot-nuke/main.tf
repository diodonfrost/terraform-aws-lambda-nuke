# Terraform to create spot instance request and spot fleet request

# Get ubuntu ami ID
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

# Request a spot instance at $0.03
resource "aws_spot_instance_request" "nuke" {
  count         = "2"
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  tags = {
    Name = "CheapWorker"
  }
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-spot"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}
