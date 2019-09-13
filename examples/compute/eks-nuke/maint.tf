# Get all availability zones
data "aws_availability_zones" "available" {
}

# Create vpc for EKS cluster
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Create subnets for EKS cluster
resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
}

resource "aws_subnet" "secondary" {
  availability_zone = data.aws_availability_zones.available.names[1]
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
}

# Create role for EKS cluster
resource "aws_iam_role" "nuke_eks" {
  name = "nuke-eks-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY

}

resource "aws_iam_role_policy_attachment" "nuke_eks_1" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.nuke_eks.name
}

resource "aws_iam_role_policy_attachment" "nuke_eks_2" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.nuke_eks.name
}

# Create EKS cluster
resource "aws_eks_cluster" "nuke_eks" {
  name     = "eks-nuke"
  role_arn = aws_iam_role.nuke_eks.arn

  vpc_config {
    subnet_ids = [aws_subnet.primary.id, aws_subnet.secondary.id]
  }
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-eks"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

