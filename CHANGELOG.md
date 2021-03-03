# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [2.12.1] - 2021-02-02
### Bug Fixes

* **log:** grant lambda scheduler to write log ([197387a](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/197387a155cd9fef16a73e4189454a802db94001))

## [2.12.0] - 2021-01-01
### Features

* **terraform:** add tags variable ([19bb8d4](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/19bb8d44b58766e1dfdc46096dcc4c5018f9bbc5))

## [2.11.0] - 2020-12-28
### Performance Improvements

* **python:** optimize aws_regions loop ([204e58a](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/204e58a9165ccd89a1efc9b7e8f5d2ba19a93980))
* **python:** use singleton class to initialize connection to aws ([2395f08](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/2395f08197c53d5db70417a4c3ba5750f4cdc751))

## [2.10.1] - 2020-12-20
### Bug fixes
* **terraform:** apply terraform fmt ([e10eb9f](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/e10eb9f7717aa0f3a47f4cd7d85d067e6b3e8c9b))

### CI
* **tflint:** update terraform version ([cfc0b4c](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/cfc0b4c3ccf8833ff6a3563e57da6823211b838a))
* **travis-ci:** removing travis-ci pipeline ([706bc0c](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/706bc0c545d1c2369f82f91480e2acfcfbfa66bf))

### Tests
* **sanity:** stop sanity script when error is found ([5c7ed0f](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/5c7ed0f66ca1441d8f2713ff3f99e431dbca7287))

## [2.10.0] - 2020-11-08
### Test

* **poetry:** add python pyproject.toml file ([d59483f](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/d59483f119d410282490ddcfeb8292d3c5041f38))
* **pytest:** set python_path directly in pytest.ini ([70e7b98](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/70e7b98d59b4a976701b3c791d489f18906fbf03))
* **kitchen-ci:** removing kitchen-ci test ([8722edb](https://github.com/diodonfrost/terraform-aws-lambda-nuke/commit/8722edbc417875b5d7b3f4558de6ed89571601e9))

## [2.9.0] - 2020-09-12
### Added
- Python 3.8 support
- Kafka nuke support

### Changed
- Restrict iam log group policy
- Improve security group exceptions
- Restrict cloudwatch log group policy
- Pytest: freeze moto version

## [2.8.0] - 2020-03-07
### Added
- Nuke ec2 snapshot
- Nuke ec2 ami

## [2.7.1] - 2020-02-28
### Added
- Waiting for instances in terminated state

### Changed
- Do not delete resource with no datetime if older_than not equal zero

## [2.7.0] - 2020-02-23
### Added
- Nuke emr cluster
- Nuke security group rule

## [2.6.0] - 2020-02-17
### Added
- kms support

## [2.5.0] - 2020-02-15
### Added
- Use Python type hint

### Changed
- Move Python aws exception in dedicated function
- Refactoring Python import

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

[Unreleased]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.12.1...HEAD
[2.12.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.12.0...2.12.1
[2.12.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.11.0...2.12.0
[2.11.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.10.1...2.11.0
[2.10.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.10.0...2.10.1
[2.10.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.9.0...2.10.0
[2.9.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.8.0...2.9.0
[2.8.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.7.1...2.8.0
[2.7.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.7.0...2.7.1
[2.7.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.6.0...2.7.0
[2.6.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.5.0...2.6.0
[2.5.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.4.0...2.5.0
[2.4.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.3.0...2.4.0
[2.3.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.2.0...2.3.0
[2.2.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.1.2...2.2.0
[2.1.2]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.1.1...2.1.2
[2.1.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.1.0...2.1.1
[2.1.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/0.10.0...2.0.0
[0.10.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/0.9.1...0.10.0
[0.9.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/0.9.0...0.9.1
[0.9.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/0.8.1...0.9.0
[0.8.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/0.8.0...0.8.1
[0.8.0]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/0.0.4...0.8.0
[0.0.4]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/v0.0.3...0.0.4
[v0.0.3]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/v0.0.2...v0.0.3
[v0.0.2]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/compare/v0.0.1...v0.0.2
[v0.0.1]: https://github.com/diodonfrost/terraform-aws-lambda-nuke/releases/tag/v0.0.1
