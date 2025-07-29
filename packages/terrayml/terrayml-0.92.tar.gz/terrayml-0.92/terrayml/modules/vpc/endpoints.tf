locals {
  vpc_endpoints = flatten([
      for vpc_key, vpc in var.vpc_list: [
        for vpc_endpoint_key, vpc_endpoint in vpc.vpc_endpoints: {
          vpc_key = vpc_key
          vpc_name = vpc.vpc_name
          vpc_id = aws_vpc.this[vpc.vpc_name].id

          vpc_endpoint_key = vpc_endpoint_key
          vpc_endpoint_type = vpc_endpoint.endpoint_type
          vpc_endpoint_name = vpc_endpoint.endpoint_name
          vpc_endpoint_service = vpc_endpoint.endpoint_service
          vpc_endpoint_route_tables = vpc_endpoint.route_tables
        }
      ]
    ])
}

resource "aws_vpc_endpoint" "this" {
    for_each = tomap({
        for vpc_endpoint in local.vpc_endpoints: "${vpc_endpoint.vpc_name}.${vpc_endpoint.vpc_endpoint_name}" => vpc_endpoint
    })
    vpc_id       = each.value.vpc_id
    service_name = "com.amazonaws.${var.common.aws_region}.${each.value.vpc_endpoint_service}"
    vpc_endpoint_type = each.value.vpc_endpoint_type
    route_table_ids = each.value.vpc_endpoint_type == "Gateway" ? [for route_table_name in each.value.vpc_endpoint_route_tables : aws_route_table.this["${each.value.vpc_name}.${route_table_name}"].id] : null

    tags = merge(var.common.default_tags, {
        Name = "${each.value.vpc_endpoint_name}-${var.common.environment}"
    })
}
