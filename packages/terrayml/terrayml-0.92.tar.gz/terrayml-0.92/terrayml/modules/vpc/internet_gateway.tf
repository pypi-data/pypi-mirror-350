locals {
  internet_gateways = flatten([
      for vpc_key, vpc in var.vpc_list: [
        for internet_gateway_name in vpc.internet_gateways: {
          vpc_key = vpc_key
          vpc_name = vpc.vpc_name
          vpc_id = aws_vpc.this[vpc.vpc_name].id
          internet_gateway_name = internet_gateway_name
        }
      ]
    ])

}


resource "aws_internet_gateway" "this" {
    for_each = tomap({
        for internet_gateway in local.internet_gateways: "${internet_gateway.vpc_name}.${internet_gateway.internet_gateway_name}" => internet_gateway
    })
    tags        = merge(var.common.default_tags, {
        Name = "${each.value.internet_gateway_name}-${var.common.environment}"
    })
}


resource "aws_internet_gateway_attachment" "this" {
    for_each = tomap({
        for internet_gateway in local.internet_gateways: "${internet_gateway.vpc_name}.${internet_gateway.internet_gateway_name}" => internet_gateway
    })
  internet_gateway_id = aws_internet_gateway.this["${each.value.vpc_name}.${each.value.internet_gateway_name}"].id
  vpc_id              = each.value.vpc_id
}