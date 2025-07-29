resource "aws_dynamodb_table" "this" {
  for_each      = { for key, value in var.dynamodb_list : value.table_name => value }
  name         = "${var.common.project_code}-${var.common.environment}-${each.value.table_name}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = each.value.hash_key
  range_key    = each.value.range_key != "NONE" ? each.value.range_key : null

  dynamic "attribute" {
    for_each = each.value.attributes
    content {
      name = attribute.value.name
      type = attribute.value.type
    }
  }
  dynamic "global_secondary_index" {
    for_each = each.value.global_secondary_indexes
    content {
      name               = global_secondary_index.value.name
      hash_key           = global_secondary_index.value.hash_key
      range_key          = global_secondary_index.value.range_key
      projection_type    = global_secondary_index.value.projection_type
    }
  }
  dynamic "local_secondary_index" {
    for_each = each.value.local_secondary_indexes
    content {
      name               = local_secondary_index.value.name
      range_key          = local_secondary_index.value.range_key
      projection_type    = local_secondary_index.value.projection_type
    }
  }
  tags = var.common.default_tags
}