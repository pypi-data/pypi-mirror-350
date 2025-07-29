locals {
  # Get a distinct list of Cognito user pool IDs by extracting them from cognito_arn
  triggers_with_configs = ["PreTokenGenerationConfig", "CustomSMSSender", "CustomEmailSender"]
  cognito_pool_ids = distinct([
    for e in var.lambda_events_list :
    e.event_details.cognito_arn != null ? split("/", e.event_details.cognito_arn)[1] : ""
    if e.event_type == "cognito_user_pool"
  ])

  # Build a map: user_pool_id => { trigger_type: lambda_function_arn, ... }
  cognito_trigger_by_pool = {
    for pool in local.cognito_pool_ids :
    pool => merge(merge([
      for e in var.lambda_events_list : 
      e.event_details.cognito_arn != null && split("/", e.event_details.cognito_arn)[1] == pool && e.event_details.trigger_type != "REMOVE" ?
        { (e.event_details.trigger_type) : aws_lambda_function.this[e.function_name].arn } : {}
    if e.event_type == "cognito_user_pool" && !contains(local.triggers_with_configs, e.event_details.trigger_type == null ? "non_cognito_trigger" : e.event_details.trigger_type)
    ]...),
    merge([
      for e in var.lambda_events_list : 
      e.event_details.cognito_arn != null && split("/", e.event_details.cognito_arn)[1] == pool && e.event_details.trigger_type != "REMOVE" ? 
      { (e.event_details.trigger_type) : {
          "LambdaArn":aws_lambda_function.this[e.function_name].arn,
          "LambdaVersion": e.event_details.trigger_config.lambda_version
      } } : {}
    if e.event_type == "cognito_user_pool" && contains(local.triggers_with_configs, e.event_details.trigger_type == null ? "non_cognito_trigger" : e.event_details.trigger_type )
    ]...)
    )
  }
}

resource "null_resource" "update_cognito_triggers" {
  for_each = local.cognito_trigger_by_pool

  # Using a trigger to force update if the lambda config changes
  triggers = {
    lambda_config = jsonencode(each.value)
  }

  provisioner "local-exec" {
    command = <<EOT
      aws cognito-idp update-user-pool \
        --user-pool-id ${each.key} \
        --lambda-config '${jsonencode(each.value)}' \
        --region ${var.common.aws_region} \
        --profile ${var.common.aws_profile}
    EOT
  }
}
