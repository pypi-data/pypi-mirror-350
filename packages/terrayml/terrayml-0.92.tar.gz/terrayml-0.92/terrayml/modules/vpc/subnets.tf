locals {
  subnets = flatten([
      for vpc_key, vpc in var.vpc_list: [
        for subnet_key, subnet in vpc.subnets: {
          vpc_key = vpc_key
          vpc_name = vpc.vpc_name
          vpc_id = aws_vpc.this[vpc.vpc_name].id

          subnet_key = subnet_key
          subnet_name = subnet.subnet_name
          subnet_cidr_block = subnet.subnet_cidr_block
          availability_zone = subnet.availability_zone
        }
      ]
    ])
}


resource "aws_subnet" "this" {
    for_each = tomap({
        for subnet in local.subnets: "${subnet.vpc_name}.${subnet.subnet_name}" => subnet
    })

    vpc_id                  = each.value.vpc_id
    cidr_block              = each.value.subnet_cidr_block
    availability_zone       = each.value.availability_zone
    tags                    = merge(var.common.default_tags, {
        Name = "${each.value.subnet_name}-${var.common.environment}"
    })
}