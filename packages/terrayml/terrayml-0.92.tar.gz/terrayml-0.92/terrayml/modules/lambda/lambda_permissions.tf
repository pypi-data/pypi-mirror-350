resource "aws_lambda_permission" "lambda_eventbridge_permission" {
  for_each      = { for key, value in var.lambda_events_list : value.function_name => value if value.event_type == "event_bridge"}

  statement_id  = "AllowEventBridgeInvocation"
  action        = "lambda:InvokeFunction"
  function_name = "${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-${var.common.environment}"
  principal     = "events.amazonaws.com"
  source_arn    = each.value.event_details.execution_arn

  depends_on = [ aws_lambda_function.this ]
}

resource "aws_lambda_permission" "lambda_apigw_permission" {
  for_each      = { for key, value in var.lambda_events_list : value.function_name => value if value.event_type == "http"}
  
  statement_id  = "${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-${var.common.environment}-AllowAPIGWInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-${var.common.environment}"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn    = "${var.apigw_execution_arns[each.value.event_details.api_gateway]}/*/*"

  depends_on = [ aws_lambda_function.this ]
}

resource "aws_lambda_permission" "lambda_cognito_permission" {
  for_each      = { for key, value in var.lambda_events_list : value.function_name => value if value.event_type == "cognito_user_pool"}

  statement_id  = "${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-${var.common.environment}-AllowCognitoInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-${var.common.environment}"
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = each.value.event_details.cognito_arn

  depends_on = [ aws_lambda_function.this ]
}