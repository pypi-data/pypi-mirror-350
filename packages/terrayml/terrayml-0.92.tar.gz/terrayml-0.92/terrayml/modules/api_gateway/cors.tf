locals {
  # Create a list of unique composite keys in the format "path::api_gateway_name"
  unique_groups = distinct([
    for lambda in var.api_gateway_lambda_list : "${lambda.path}::${lambda.api_gateway_name}"
  ])

  # For each unique combination, extract the details and the distinct methods
  lambda_groups = {
    for group in local.unique_groups : group => {
      path             = split("::", group)[0]
      api_gateway_name = split("::", group)[1]
      methods = distinct([
        for lambda in var.api_gateway_lambda_list :
        lambda.method if lambda.path == split("::", group)[0] && lambda.api_gateway_name == split("::", group)[1]
      ])
    }
  }
}

resource "aws_api_gateway_method" "cors_options" {
  # One OPTIONS resource per unique path & API Gateway combination
  for_each = local.lambda_groups

  rest_api_id   = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
  resource_id   = local.api_gateway_resources[each.value.path]
  http_method   = "OPTIONS"
  authorization = "NONE"
}
resource "aws_api_gateway_integration" "cors_integration" {
  for_each = local.lambda_groups

  rest_api_id   = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
  resource_id   = local.api_gateway_resources[each.value.path]
  http_method   = aws_api_gateway_method.cors_options[each.key].http_method
  type          = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }

  depends_on = [ aws_api_gateway_method.cors_options ]
}

resource "aws_api_gateway_method_response" "cors_method_response" {
  for_each = local.lambda_groups

  rest_api_id   = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
  resource_id   = local.api_gateway_resources[each.value.path]
  http_method   = aws_api_gateway_method.cors_options[each.key].http_method
  status_code   = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }

  depends_on = [ aws_api_gateway_method.cors_options ]
}

resource "aws_api_gateway_integration_response" "cors_integration_response" {
  for_each = local.lambda_groups

  rest_api_id   = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
  resource_id   = local.api_gateway_resources[each.value.path]
  http_method   = aws_api_gateway_method.cors_options[each.key].http_method
  status_code   = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'"
    "method.response.header.Access-Control-Allow-Methods" = "'${join(",", each.value.methods)},OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [ aws_api_gateway_method_response.cors_method_response ]
}
