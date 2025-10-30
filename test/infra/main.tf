# fixture
module "backend_router" {
  source = "../.."

  team                    = var.team
  env                     = var.env
  component               = var.component
  platform_config         = var.platform_config

  run_data                = false
  certificate_domain_name = "*.domain.com"
}

module "backend_router_external" {
  source = "../.."

  team                    = var.team
  env                     = var.env
  component               = var.component
  platform_config         = var.platform_config
  alb_internal            = "false"

  run_data                = false
  certificate_domain_name = "*.domain.com"
}

# configure provider to not try too hard talking to AWS API
provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

# variables
variable "team" {}

variable "env" {}

variable "component" {}

variable "platform_config" {
  type = map(string)
}

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.99.1"
    }
  }
}