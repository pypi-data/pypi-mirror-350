locals {
  nat_gateways = flatten([
      for vpc_key, vpc in var.vpc_list: [
        for nat_gateway_key, nat_gateway in vpc.nat_gateways: {
          vpc_key = vpc_key
          vpc_name = vpc.vpc_name
          vpc_id = aws_vpc.this[vpc.vpc_name].id

          nat_gateway_key = nat_gateway_key
          nat_gateway_name = nat_gateway.nat_gateway_name
          nat_gateway_subnet = nat_gateway.subnet
        }
      ]
    ])

}

resource "aws_nat_gateway" "this" {
    for_each = tomap({
        for nat_gateway in local.nat_gateways: "${nat_gateway.vpc_name}.${nat_gateway.nat_gateway_name}" => nat_gateway
    })
    allocation_id = aws_eip.this["${each.value.vpc_name}.${each.value.nat_gateway_name}"].allocation_id
    subnet_id     = aws_subnet.this["${each.value.vpc_name}.${each.value.nat_gateway_subnet}"].id

    tags = merge(var.common.default_tags, {
        Name = "${each.value.nat_gateway_name}-${var.common.environment}"
    })

  # To ensure proper ordering, it is recommended to add an explicit dependency
  # on the Internet Gateway for the VPC.
  depends_on = [aws_internet_gateway.this, aws_eip.this]
}

resource "aws_eip" "this" {
    for_each = tomap({
        for nat_gateway in local.nat_gateways: "${nat_gateway.vpc_name}.${nat_gateway.nat_gateway_name}" => nat_gateway
    })
    domain  = "vpc"
    tags = merge(var.common.default_tags, {
        Name = "${each.value.nat_gateway_name}-eip-${var.common.environment}"
    })
}