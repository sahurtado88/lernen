provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Entorno   = var.environment
      Terraform = true

    }
  }
}

terraform {
  backend "s3" {
    bucket  = "mi-bucket-terraform-statebelcorp"
    key     = "state/test.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}



terraform {
  required_version = "~> 1.12.2"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.13.0"
    }
  }
}
