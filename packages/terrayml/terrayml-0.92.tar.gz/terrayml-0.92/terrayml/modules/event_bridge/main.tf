resource "aws_cloudwatch_event_rule" "this" {
    for_each        = { for key, value in var.event_bridge_rule_list: value.event_bridge_rule_name => value }
    name            = "${var.common.project_code}-${var.common.service_name}-${var.common.environment}-${each.value.event_bridge_rule_name}-rule"
    event_bus_name  = each.value.event_bridge_rule_target_bus_name
    description     = "Event Bridge Rule"
    event_pattern   = jsonencode({
        "source" : each.value.event_bridge_rule_source,
        "detail-type" : each.value.event_bridge_rule_detail_type
    })
    tags            = var.common.default_tags
}

resource "aws_cloudwatch_event_target" "this" {
    for_each = { for key, value in var.event_bridge_rule_list: value.event_bridge_rule_name => value }

    rule            = aws_cloudwatch_event_rule.this[each.value.event_bridge_rule_name].name
    target_id       = "${aws_cloudwatch_event_rule.this[each.value.event_bridge_rule_name].name}-target"
    arn             = each.value.event_bridge_rule_target_arn
    event_bus_name  = each.value.event_bridge_rule_target_bus_name
}

resource "aws_cloudwatch_event_bus" "this" {
    for_each    = { for key, value in var.event_bridge_event_bus_list : value.event_bridge_bus_name => value}
    name        = "${var.common.project_name}-${var.common.service_name}-${var.common.environment}-${each.value.event_bridge_bus_name}"
}

output "execution_rule_arns" {
  value = { for key, value in var.event_bridge_rule_list : value.event_bridge_rule_name => aws_cloudwatch_event_rule.this[value.event_bridge_rule_name].arn }
}