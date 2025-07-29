locals {
  lambda_explicit_service_policies = flatten([
    for lambda_function_key, lambda_function in var.lambda_function_list: [
      for explicit_service_policy_key, service_policy in lambda_function.explicit_service_policies: {
        lambda_function_key = lambda_function_key
        lambda_function_name = lambda_function.function_name
        explicit_service_policy_key = explicit_service_policy_key
        service_name = service_policy.service_name
        allowed_actions = service_policy.allowed_actions
        allowed_resources = service_policy.allowed_resources
      }
    ]
  ])
}

resource "aws_iam_policy" "this" {
  for_each = tomap({
    for explicit_service_policy in local.lambda_explicit_service_policies: "${explicit_service_policy.lambda_function_name}.${explicit_service_policy.service_name}" => explicit_service_policy
  })
  name        = "${var.common.project_code}-${var.common.service_name}-${each.value.lambda_function_name}-${var.common.environment}-${each.value.service_name}-policy"
  description = "Project-Service: ${var.common.project_code}-${var.common.service_name} Lambda: ${each.value.lambda_function_name} Service: ${each.value.service_name} Policy"

  policy = jsonencode(
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": each.value.allowed_actions,
                "Resource": each.value.allowed_resources,
                "Effect": "Allow"
            }
        ]
    }
  )
  tags = var.common.default_tags
}

resource "aws_iam_role_policy_attachment" "this" {
  for_each = tomap({
    for explicit_service_policy in local.lambda_explicit_service_policies: "${explicit_service_policy.lambda_function_name}.${explicit_service_policy.service_name}" => explicit_service_policy
  })
  role       = aws_iam_role.lambda-exec-role[each.value.lambda_function_name].name
  policy_arn = aws_iam_policy.this["${each.value.lambda_function_name}.${each.value.service_name}"].arn

}
