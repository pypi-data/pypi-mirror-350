locals {
  provided_full_paths = [for r in var.api_gateway_lambda_list : r.path]
  
  
  resource_paths = flatten([
    for item in var.api_gateway_lambda_list : [
      for idx, segment in split("/", item.path) : {
        full_path = item.path
        parent_path = idx == 0 ? "NONE" : join("/", slice(split("/", item.path), 0, idx))
        current_path = idx == 0 ? "NONE" : "${join("/", slice(split("/", item.path), 0, idx))}/${segment}"
        api_gateway_name = item.api_gateway_name
        path   = segment
        level  = idx + 1
      }
      if segment != ""
    ]
  ])

  composite_keys = [for o in local.resource_paths : "${o.parent_path}-${o.path}-${o.level}"]
  unique_split_paths = [
    for idx, obj in local.resource_paths : obj
    if index(local.composite_keys, "${obj.parent_path}-${obj.path}-${obj.level}") == idx
  ]
  depth1 = { for k, v in local.unique_split_paths : v.current_path => v if v.level == 2 }
  depth2 = { for k, v in local.unique_split_paths : v.current_path => v if v.level == 3 }
  depth3 = { for k, v in local.unique_split_paths : v.current_path => v if v.level == 4 }
  depth4 = { for k, v in local.unique_split_paths : v.current_path => v if v.level == 5 }
  depth5 = { for k, v in local.unique_split_paths : v.current_path => v if v.level == 6 }
}

resource "aws_api_gateway_resource" "depth1" {
  for_each = local.depth1

  path_part   = each.value.path
  parent_id   = aws_api_gateway_rest_api.this[each.value.api_gateway_name].root_resource_id
  rest_api_id = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
}

resource "aws_api_gateway_resource" "depth2" {
  for_each = local.depth2

  path_part = each.value.path
  parent_id = aws_api_gateway_resource.depth1[each.value.parent_path].id
  rest_api_id = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
}
resource "aws_api_gateway_resource" "depth3" {
  for_each = local.depth3

  path_part = each.value.path
  parent_id = aws_api_gateway_resource.depth2[each.value.parent_path].id
  rest_api_id = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
}
resource "aws_api_gateway_resource" "depth4" {
  for_each = local.depth4

  path_part = each.value.path
  parent_id = aws_api_gateway_resource.depth3[each.value.parent_path].id
  rest_api_id = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
}
resource "aws_api_gateway_resource" "depth5" {
  for_each = local.depth5

  path_part = each.value.path
  parent_id = aws_api_gateway_resource.depth4[each.value.parent_path].id
  rest_api_id = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
}
