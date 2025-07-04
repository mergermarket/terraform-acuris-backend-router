module "alb" {
  source  = "mergermarket/alb/acuris"
  version = "2.2.1"

  name   = format("%s-%s-router", var.env, var.component)
  vpc_id = var.platform_config["vpc"]
  subnet_ids = split(
    ",",
    var.alb_internal ? var.platform_config["private_subnets"] : var.platform_config["public_subnets"],
  )
  internal = var.alb_internal
  extra_security_groups = concat(
    [
      var.platform_config["ecs_cluster.default.client_security_group"],
    ],
    var.extra_security_groups,
  )
  certificate_domain_name  = var.certificate_domain_name
  run_data                 = var.run_data
  default_target_group_arn = aws_alb_target_group.default_target_group.arn
  access_logs_bucket       = lookup(var.platform_config, "elb_access_logs_bucket", "")
  access_logs_enabled      = lookup(var.platform_config, "elb_access_logs_bucket", "") == "" ? false : true
  idle_timeout             = var.idle_timeout
  tags = {
    component   = var.component
    environment = var.env
    team        = var.team
  }
}

resource "aws_alb_target_group" "default_target_group" {
  name = replace(
    replace(
      replace("${var.env}-default-${var.component}", "/(.{0,32}).*/", "$1"),
    "/^-+|-+$/",
    ""),
  "_","-")

  # port will be set dynamically, but for some reason AWS requires a value
  port                 = "31337"
  protocol             = "HTTP"
  vpc_id               = var.platform_config["vpc"]
  deregistration_delay = var.default_target_group_deregistration_delay

  health_check {
    interval            = var.default_target_group_health_check_interval
    path                = var.default_target_group_health_check_path
    timeout             = var.default_target_group_health_check_timeout
    healthy_threshold   = var.default_target_group_health_check_healthy_threshold
    unhealthy_threshold = var.default_target_group_health_check_unhealthy_threshold
    matcher             = var.default_target_group_health_check_matcher
  }
}

