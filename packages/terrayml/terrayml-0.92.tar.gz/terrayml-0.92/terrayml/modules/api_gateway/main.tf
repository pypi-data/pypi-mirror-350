locals {
  apigw_authorizers = flatten([
    for api_gateway_key, api_gateway in var.api_gateway_list: [
      for authorizer_key, authorizer in api_gateway.authorizers: {
        api_gateway_key = api_gateway_key
        api_gateway_name = api_gateway.api_gateway_name
        authorizer_key = authorizer_key
        authorizer_name = authorizer.authorizer_name
        authorizer_type = authorizer.authorizer_type
        authorizer_provider_arns = authorizer.authorizer_provider_arns
        authorizer_identity_source = authorizer.authorizer_identity_source
      }
    ]
  ])
  api_gateway_resources = merge(
    { for k, r in aws_api_gateway_resource.depth1 : k => r.id },
    { for k, r in aws_api_gateway_resource.depth2 : k => r.id },
    { for k, r in aws_api_gateway_resource.depth3 : k => r.id },
    { for k, r in aws_api_gateway_resource.depth4 : k => r.id },
    { for k, r in aws_api_gateway_resource.depth5 : k => r.id }
  )
}

resource "aws_api_gateway_rest_api" "this" {
    for_each = { for key, value in var.api_gateway_list : value.api_gateway_name => value}
    name        = "${var.common.project_code}-${each.value.api_gateway_name}-${var.common.environment}"
}
resource "aws_api_gateway_authorizer" "apigw_authorizer" {
    for_each = tomap({
      for authorizer in local.apigw_authorizers: "${authorizer.api_gateway_name}.${authorizer.authorizer_name}" => authorizer
    })
    name                   = "${aws_api_gateway_rest_api.this[each.value.api_gateway_name].name}-${each.value.authorizer_name}"
    rest_api_id            = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
    type                   = each.value.authorizer_type
    provider_arns          = each.value.authorizer_provider_arns
    identity_source        = each.value.authorizer_identity_source
    # identity_source        = "method.request.header.Authorization"
}
# resource "aws_api_gateway_resource" "lambda_apigw_resources" {
#     for_each = { for key, value in var.api_gateway_lambda_list : "${value.function_name}.${value.path}" => value }
#     path_part   = each.value.path
#     parent_id   = each.value.parent_path == each.value.path ? aws_api_gateway_rest_api.this[each.value.api_gateway_name].root_resource_id : aws_api_gateway_resource.lambda_apigw_resources["${each.value.function_name}.${each.value.parent_path}"].id
#     rest_api_id = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id

# }

resource "aws_api_gateway_method" "lambda_apigw_method" {
    for_each = { for key, value in var.api_gateway_lambda_list : value.function_name => value}

    rest_api_id   = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
    resource_id   = local.api_gateway_resources[each.value.path]
    http_method   = each.value.method
    authorization = each.value.authorizer_type # NONE, CUSTOM, AWS_IAM or COGNITO_USER_POOLS
    authorizer_id = each.value.authorizer_type != "NONE" ? aws_api_gateway_authorizer.apigw_authorizer["${each.value.api_gateway_name}.${each.value.authorizer_name}"].id : null

    authorization_scopes = each.value.authorization_scopes
}

resource "aws_api_gateway_integration" "integration" {
    for_each =  { for key, value in var.api_gateway_lambda_list : value.function_name => value}

    rest_api_id             = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
    resource_id             = local.api_gateway_resources[each.value.path]
    http_method             = each.value.method
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = each.value.invoke_arn

    depends_on = [ aws_api_gateway_resource.depth1, aws_api_gateway_resource.depth2, aws_api_gateway_resource.depth3, aws_api_gateway_resource.depth4, aws_api_gateway_resource.depth5, aws_api_gateway_method.lambda_apigw_method ]
}


resource "aws_api_gateway_deployment" "this" {
  for_each = length(var.api_gateway_lambda_list) > 0 ? { for key, value in var.api_gateway_list : value.api_gateway_name => value} : {}
  rest_api_id = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_rest_api.this[each.value.api_gateway_name].body,
      aws_api_gateway_method.lambda_apigw_method,
      aws_api_gateway_integration.integration,
      aws_api_gateway_integration.cors_integration]))
  }
  depends_on = [ aws_api_gateway_integration.integration, aws_api_gateway_integration.cors_integration ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "this" {
  for_each = length(var.api_gateway_lambda_list) > 0 ? { for key, value in var.api_gateway_list : value.api_gateway_name => value} : {}

  deployment_id = aws_api_gateway_deployment.this[each.value.api_gateway_name].id
  rest_api_id   = aws_api_gateway_rest_api.this[each.value.api_gateway_name].id
  stage_name    = var.common.environment
}
output "apigw_execution_arns" {
  value = { for key, value in var.api_gateway_list : value.api_gateway_name => aws_api_gateway_rest_api.this[value.api_gateway_name].execution_arn }
}
# output "apigw_endpoints" {
#   value = { for key, value in var.api_gateway_list : value.api_gateway_name => aws_api_gateway_rest_api.this[value.api_gateway_name].api_endpoint }
# }
# output "apigw_endpoint" {
#   value = aws_apigatewayv2_api.apigw.api_endpoint
# }