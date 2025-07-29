
resource "aws_vpc" "this" {
  for_each    = { for key, value in var.vpc_list : value.vpc_name => value }
  cidr_block           = each.value.cidr_block
  tags        = merge(var.common.default_tags, {
    Name = "${each.value.vpc_name}-${var.common.environment}"
  })
}

