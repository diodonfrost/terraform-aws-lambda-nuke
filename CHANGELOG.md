# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [2.4.0] - 2020-02-01
### Added
- Multi aws region support

## [2.3.0] - 2019-10-29
### Changed
- Allow empty value for terraform variable exclude_resources

### Removed
- Duplicated rds api call

## [2.2.0] - 2019-10-19
### Added
- Nuke s3 object version
- Python unit tests

## [2.1.2] - 2019-10-06
### Changed
- Optimize python code with yield

## [2.1.1] - 2019-10-04
## Changed
- Python poo style

## [2.1.0] - 2019-09-14
### Added
- Custom IAM role

## [2.0.0] - 2019-09-13
### Added
- Terraform 0.12 support
- AWS cloudwatch dashboard and alarm deletion

### Changed
- Reduce complexicy of main function

## [0.10.0] - 2019-08-11
### Added
- Tox ci
- Pylint convention
- Flake8 convention
- Black formating
- Force UTF-8

### Changed
- Reduce complexity of Python code
- Refactoring whole Python code
- Fix EFS nuke function

## [0.9.1] - 2019-07-05
### Added
- Spot deletion support
- Classic loadbalancer deletion support

### Changed
- Delete s3 bucket with objects
- Don't delete s3 bucket with policy
- Refactoring python logging
- Use local module in Terraform examples

### Removed
- AWS nat gateway deletion
- AWS internet gateway deletion
- AWS route table deletion

## [0.9.0] - 2019-06-19
### Added
- Paginator for Python launch_configuration resources

### Changed
- Refactoring all Python exception handling
- Fix Python dlm nuke function
- Update aws update availability zones in Terraform examples
- Fix Terraform CloudWatch policy

## [0.8.1] - 2019-06-17
### Added
- Enable CloudWatch loggings

### Changed
- Fix s3 objects deletion

## [0.8.0] - 2019-06-15
### Added
- Sonarqube scan

### Changed
- Improve order deletion
- Refactoring python code

## [0.0.4] - 2019-05-09
### Changed
- Improve awspec tests
- Use inline policy instead of custom managed policy
- Set default aws region to eu-west-1

## [v0.0.3] - 2019-04-17
### Added
- AWS eip deletion support
- AWS endpoint deletion support
- AWS internet gateway deletion support
- AWS nat gateway deletion support
- AWS route table deletion support
- AWS security group and acl deletion support

## [v0.0.2] - 2019-03-15
### Added
- AWS dynamodb deletion support
- AWS elasticache deletion support
- AWS neptune deletion support
- AWS rds deletion support
- AWS redshift deletion support

## [v0.0.1] - 2019-03-07
### Added
- AWS autoscaling group deletion support
- AWS ebs deletion support
- AWS ec2 instances deletion support
- AWS ecr deletion support
- AWS ecs deletion support
- AWS eks deletion support
- AWS elasticbeanstalk deletion support
- AWS elbv2 deletion support
- AWS keypair deletion support

[Unreleased]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/2.4.0...HEAD
[2.4.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/2.3.0...2.4.0
[2.3.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/2.2.0...2.3.0
[2.2.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/2.1.2...2.2.0
[2.1.2]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/2.1.1...2.1.2
[2.1.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/2.1.0...2.1.1
[2.1.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/2.0.0...2.1.0
[2.0.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/0.10.0...2.0.0
[0.10.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/0.9.1...0.10.0
[0.9.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/0.9.0...0.9.1
[0.9.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/0.8.1...0.9.0
[0.8.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/0.8.0...0.8.1
[0.8.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/0.0.4...0.8.0
[0.0.4]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/v0.0.3...0.0.4
[v0.0.3]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/v0.0.2...v0.0.3
[v0.0.2]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/v0.0.1...v0.0.2
[v0.0.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/releases/tag/v0.0.1
