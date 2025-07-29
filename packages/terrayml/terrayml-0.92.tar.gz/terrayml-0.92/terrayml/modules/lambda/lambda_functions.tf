resource "aws_lambda_function" "this" {
  for_each      = { for key, value in var.lambda_function_list : value.function_name => value }

  s3_bucket     = aws_s3_bucket.lambda_s3.bucket
  s3_key        = aws_s3_object.this.key
  function_name = "${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-${var.common.environment}"
  description   = each.value.description
  role          = aws_iam_role.lambda-exec-role[each.value.function_name].arn
  handler       = each.value.handler
  layers        = toset(concat([aws_lambda_layer_version.this.arn], each.value.custom_layers))
  runtime       = each.value.runtime
  memory_size   = each.value.memory_size
  timeout       = each.value.timeout

  source_code_hash = data.archive_file.this.output_base64sha256
  
  vpc_config {
    subnet_ids         = each.value.vpc_config.subnet_ids
    security_group_ids = each.value.vpc_config.security_group_ids
  }

  environment {
    variables = each.value.variables
  }

  tags = var.common.default_tags

  depends_on = [ aws_iam_role.lambda-exec-role ]

}

output "lambda_arns" {
  value = { for key, value in var.lambda_function_list : value.function_name => aws_lambda_function.this[value.function_name].arn }
}
output "lambda_invoke_arns" {
  value = { for key, value in var.lambda_function_list : value.function_name => aws_lambda_function.this[value.function_name].invoke_arn }
}