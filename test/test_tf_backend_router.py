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
      + arn                                                          = (known after apply)
      + arn_suffix                                                   = (known after apply)
      + client_keep_alive                                            = 3600
      + desync_mitigation_mode                                       = "defensive"
      + dns_name                                                     = (known after apply)
      + drop_invalid_header_fields                                   = false
      + enable_deletion_protection                                   = false
      + enable_http2                                                 = true
      + enable_tls_version_and_cipher_suite_headers                  = false
      + enable_waf_fail_open                                         = false
      + enable_xff_client_port                                       = false
      + enable_zonal_shift                                           = false
      + enforce_security_group_inbound_rules_on_private_link_traffic = (known after apply)
      + id                                                           = (known after apply)
      + idle_timeout                                                 = 60
      + internal                                                     = true
      + ip_address_type                                              = (known after apply)
      + load_balancer_type                                           = "application"
      + name                                                         = "dev-foobar-router"
      + name_prefix                                                  = (known after apply)
      + preserve_host_header                                         = false
      + region                                                       = "eu-west-1"
      + secondary_ips_auto_assigned_per_subnet                       = (known after apply)
      + security_groups                                              = (known after apply)
      + subnets                                                      = [
          + "subnet-00000000",
          + "subnet-11111111",
          + "subnet-22222222",
        ]
      + tags                                                         = {
          + "component"   = "foobar"
          + "environment" = "dev"
          + "team"        = "foobar"
        }
      + tags_all                                                     = {
          + "component"   = "foobar"
          + "environment" = "dev"
          + "team"        = "foobar"
        }
      + vpc_id                                                       = (known after apply)
      + xff_header_processing_mode                                   = "append"
      + zone_id                                                      = (known after apply)

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
      + arn                                                                   = (known after apply)
      + id                                                                    = (known after apply)
      + load_balancer_arn                                                     = (known after apply)
      + port                                                                  = 443
      + protocol                                                              = "HTTPS"
      + region                                                                = "eu-west-1"
      + routing_http_request_x_amzn_mtls_clientcert_header_name               = (known after apply)
      + routing_http_request_x_amzn_mtls_clientcert_issuer_header_name        = (known after apply)
      + routing_http_request_x_amzn_mtls_clientcert_leaf_header_name          = (known after apply)
      + routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name = (known after apply)
      + routing_http_request_x_amzn_mtls_clientcert_subject_header_name       = (known after apply)
      + routing_http_request_x_amzn_mtls_clientcert_validity_header_name      = (known after apply)
      + routing_http_request_x_amzn_tls_cipher_suite_header_name              = (known after apply)
      + routing_http_request_x_amzn_tls_version_header_name                   = (known after apply)
      + routing_http_response_access_control_allow_credentials_header_value   = (known after apply)
      + routing_http_response_access_control_allow_headers_header_value       = (known after apply)
      + routing_http_response_access_control_allow_methods_header_value       = (known after apply)
      + routing_http_response_access_control_allow_origin_header_value        = (known after apply)
      + routing_http_response_access_control_expose_headers_header_value      = (known after apply)
      + routing_http_response_access_control_max_age_header_value             = (known after apply)
      + routing_http_response_content_security_policy_header_value            = (known after apply)
      + routing_http_response_server_enabled                                  = (known after apply)
      + routing_http_response_strict_transport_security_header_value          = (known after apply)
      + routing_http_response_x_content_type_options_header_value             = (known after apply)
      + routing_http_response_x_frame_options_header_value                    = (known after apply)
      + ssl_policy                                                            = "ELBSecurityPolicy-TLS13-1-2-Res-2021-06"
      + tags_all                                                              = (known after apply)
      + tcp_idle_timeout_seconds                                              = (known after apply)

      + default_action {
          + order            = (known after apply)
          + target_group_arn = (known after apply)
          + type             = "forward"
        }

      + mutual_authentication {
          + advertise_trust_store_ca_names   = (known after apply)
          + ignore_client_certificate_expiry = (known after apply)
          + mode                             = (known after apply)
          + trust_store_arn                  = (known after apply)
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
      + region                 = "eu-west-1"
      + revoke_rules_on_delete = false
      + tags_all               = (known after apply)
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
      + arn                                                          = (known after apply)
      + arn_suffix                                                   = (known after apply)
      + client_keep_alive                                            = 3600
      + desync_mitigation_mode                                       = "defensive"
      + dns_name                                                     = (known after apply)
      + drop_invalid_header_fields                                   = false
      + enable_deletion_protection                                   = false
      + enable_http2                                                 = true
      + enable_tls_version_and_cipher_suite_headers                  = false
      + enable_waf_fail_open                                         = false
      + enable_xff_client_port                                       = false
      + enable_zonal_shift                                           = false
      + enforce_security_group_inbound_rules_on_private_link_traffic = (known after apply)
      + id                                                           = (known after apply)
      + idle_timeout                                                 = 60
      + internal                                                     = false
      + ip_address_type                                              = (known after apply)
      + load_balancer_type                                           = "application"
      + name                                                         = "dev-foobar-router"
      + name_prefix                                                  = (known after apply)
      + preserve_host_header                                         = false
      + region                                                       = "eu-west-1"
      + secondary_ips_auto_assigned_per_subnet                       = (known after apply)
      + security_groups                                              = (known after apply)
      + subnets                                                      = [
          + "subnet-33333333",
          + "subnet-44444444",
          + "subnet-555555555",
        ]
      + tags                                                         = {
          + "component"   = "foobar"
          + "environment" = "dev"
          + "team"        = "foobar"
        }
      + tags_all                                                     = {
          + "component"   = "foobar"
          + "environment" = "dev"
          + "team"        = "foobar"
        }
      + vpc_id                                                       = (known after apply)
      + xff_header_processing_mode                                   = "append"
      + zone_id                                                      = (known after apply)

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
      + connection_termination             = (known after apply)
      + deregistration_delay               = "10"
      + id                                 = (known after apply)
      + ip_address_type                    = (known after apply)
      + lambda_multi_value_headers_enabled = false
      + load_balancer_arns                 = (known after apply)
      + load_balancing_algorithm_type      = (known after apply)
      + load_balancing_anomaly_mitigation  = (known after apply)
      + load_balancing_cross_zone_enabled  = (known after apply)
      + name                               = "dev-default-foobar"
      + name_prefix                        = (known after apply)
      + port                               = 31337
      + preserve_client_ip                 = (known after apply)
      + protocol                           = "HTTP"
      + protocol_version                   = (known after apply)
      + proxy_protocol_v2                  = false
      + region                             = "eu-west-1"
      + slow_start                         = 0
      + tags_all                           = (known after apply)
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
          + cookie_name     = (known after apply)
          + enabled         = (known after apply)
          + type            = (known after apply)
        }

      + target_failover {
          + on_deregistration = (known after apply)
          + on_unhealthy      = (known after apply)
        }

      + target_group_health {
          + dns_failover {
              + minimum_healthy_targets_count      = (known after apply)
              + minimum_healthy_targets_percentage = (known after apply)
            }

          + unhealthy_state_routing {
              + minimum_healthy_targets_count      = (known after apply)
              + minimum_healthy_targets_percentage = (known after apply)
            }
        }

      + target_health_state {
          + enable_unhealthy_connection_termination = (known after apply)
          + unhealthy_draining_interval             = (known after apply)
        }
    }
        """.strip() in output # noqa
