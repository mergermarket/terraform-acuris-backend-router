import unittest
from subprocess import check_call, check_output


class TestTFBackendRouter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        check_call(['terraform', 'init'])
        return super().setUpClass()

    def setUp(self):
        check_call(['terraform', 'get', 'test/infra'])

    def test_create_backend_router_number_of_resources_to_add(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_router.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
Plan: 4 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_create_alb(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_router.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
  # module.backend_router.module.alb.aws_alb.alb will be created
  + resource "aws_alb" "alb" {
      + arn                        = (known after apply)
      + arn_suffix                 = (known after apply)
      + dns_name                   = (known after apply)
      + drop_invalid_header_fields = false
      + enable_deletion_protection = false
      + enable_http2               = true
      + id                         = (known after apply)
      + idle_timeout               = 60
      + internal                   = true
      + ip_address_type            = (known after apply)
      + load_balancer_type         = "application"
      + name                       = "dev-foobar-router"
      + security_groups            = (known after apply)
      + subnets                    = [
          + "subnet-00000000",
          + "subnet-11111111",
          + "subnet-22222222",
        ]
      + tags                       = {
          + "component"   = "foobar"
          + "environment" = "dev"
          + "team"        = "foobar"
        }
      + vpc_id                     = (known after apply)
      + zone_id                    = (known after apply)

      + access_logs {
          + enabled = false
        }

      + subnet_mapping {
          + allocation_id        = (known after apply)
          + ipv6_address         = (known after apply)
          + outpost_id           = (known after apply)
          + private_ipv4_address = (known after apply)
          + subnet_id            = (known after apply)
        }
    }
        """.strip() in output # noqa

    def test_create_alb_listener(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_router.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
  # module.backend_router.module.alb.aws_alb_listener.https will be created
  + resource "aws_alb_listener" "https" {
      + arn               = (known after apply)
      + id                = (known after apply)
      + load_balancer_arn = (known after apply)
      + port              = 443
      + protocol          = "HTTPS"
      + ssl_policy        = (known after apply)

      + default_action {
          + order            = (known after apply)
          + target_group_arn = (known after apply)
          + type             = "forward"
        }
    }
        """.strip() in output # noqa

    def test_create_alb_security_group(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_router.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
  # module.backend_router.module.alb.aws_security_group.default will be created
  + resource "aws_security_group" "default" {
      + arn                    = (known after apply)
      + description            = "Managed by Terraform"
      + egress                 = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = ""
              + from_port        = 0
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "-1"
              + security_groups  = []
              + self             = false
              + to_port          = 0
            },
        ]
      + id                     = (known after apply)
      + ingress                = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = ""
              + from_port        = 443
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 443
            },
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = ""
              + from_port        = 80
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 80
            },
        ]
      + name                   = (known after apply)
      + name_prefix            = (known after apply)
      + owner_id               = (known after apply)
      + revoke_rules_on_delete = false
      + vpc_id                 = "vpc-12345678"
    }
        """.strip() in output # noqa

    def test_create_external_alb(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_router_external.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
  # module.backend_router_external.module.alb.aws_alb.alb will be created
  + resource "aws_alb" "alb" {
      + arn                        = (known after apply)
      + arn_suffix                 = (known after apply)
      + dns_name                   = (known after apply)
      + drop_invalid_header_fields = false
      + enable_deletion_protection = false
      + enable_http2               = true
      + id                         = (known after apply)
      + idle_timeout               = 60
      + internal                   = false
      + ip_address_type            = (known after apply)
      + load_balancer_type         = "application"
      + name                       = "dev-foobar-router"
      + security_groups            = (known after apply)
      + subnets                    = [
          + "subnet-33333333",
          + "subnet-44444444",
          + "subnet-555555555",
        ]
      + tags                       = {
          + "component"   = "foobar"
          + "environment" = "dev"
          + "team"        = "foobar"
        }
      + vpc_id                     = (known after apply)
      + zone_id                    = (known after apply)

      + access_logs {
          + enabled = false
        }

      + subnet_mapping {
          + allocation_id        = (known after apply)
          + ipv6_address         = (known after apply)
          + outpost_id           = (known after apply)
          + private_ipv4_address = (known after apply)
          + subnet_id            = (known after apply)
        }
    }
        """.strip() in output # noqa

    def test_default_target_group(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_router',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
  # module.backend_router.aws_alb_target_group.default_target_group will be created
  + resource "aws_alb_target_group" "default_target_group" {
      + arn                                = (known after apply)
      + arn_suffix                         = (known after apply)
      + deregistration_delay               = 10
      + id                                 = (known after apply)
      + lambda_multi_value_headers_enabled = false
      + load_balancing_algorithm_type      = (known after apply)
      + name                               = "dev-default-foobar"
      + port                               = 31337
      + preserve_client_ip                 = (known after apply)
      + protocol                           = "HTTP"
      + protocol_version                   = (known after apply)
      + proxy_protocol_v2                  = false
      + slow_start                         = 0
      + target_type                        = "instance"
      + vpc_id                             = "vpc-12345678"

      + health_check {
          + enabled             = true
          + healthy_threshold   = 2
          + interval            = 5
          + matcher             = "200-299"
          + path                = "/internal/healthcheck"
          + port                = "traffic-port"
          + protocol            = "HTTP"
          + timeout             = 4
          + unhealthy_threshold = 2
        }

      + stickiness {
          + cookie_duration = (known after apply)
          + enabled         = (known after apply)
          + type            = (known after apply)
        }
    }
        """.strip() in output # noqa
