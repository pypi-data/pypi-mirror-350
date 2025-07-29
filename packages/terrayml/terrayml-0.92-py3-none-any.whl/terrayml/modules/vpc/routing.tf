locals {
  route_tables = flatten([
      for vpc_key, vpc in var.vpc_list: [
        for route_table_key, route_table in vpc.route_tables: {
            vpc_key = vpc_key
            vpc_name = vpc.vpc_name
            vpc_id = aws_vpc.this[vpc.vpc_name].id
            
            route_table_name = route_table.route_table_name
            routes = route_table.routes
        }
      ]
    ])
  subnet_associations = flatten([
      for vpc_key, vpc in var.vpc_list: [
        for route_table_key, route_table in vpc.route_tables: [
            for subnet in route_table.subnets: {
                vpc_key = vpc_key
                vpc_name = vpc.vpc_name
                vpc_id = aws_vpc.this[vpc.vpc_name].id

                route_table_name = route_table.route_table_name
                subnet_name = subnet
            }
        ]
      ]
    ])
}


resource "aws_route_table" "this" {
    for_each = tomap({
        for route_table in local.route_tables: "${route_table.vpc_name}.${route_table.route_table_name}" => route_table
    })
    vpc_id      = each.value.vpc_id
    tags        = merge(var.common.default_tags, {
        Name = "${each.value.route_table_name}-${var.common.environment}"
    })
    dynamic "route" {
        for_each = each.value.routes

        content {
            cidr_block = route.value.destination_cidr_block

            gateway_id = (
                    route.value.target_type == "local") ? route.value.target : (
                    route.value.target_type == "internet_gateway")   ? aws_internet_gateway.this["${each.value.vpc_name}.${route.value.target}"].id : (
                    route.value.target_type == "nat_gateway") ? aws_nat_gateway.this["${each.value.vpc_name}.${route.value.target}"].id: null
        }
    }
}

resource "aws_route_table_association" "this" {
    for_each = tomap({
        for subnet_association in local.subnet_associations: "${subnet_association.vpc_name}.${subnet_association.subnet_name}" => subnet_association
    })
    subnet_id      = aws_subnet.this["${each.value.vpc_name}.${each.value.subnet_name}"].id
    route_table_id = aws_route_table.this["${each.value.vpc_name}.${each.value.route_table_name}"].id
}