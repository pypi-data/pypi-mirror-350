resource "aws_iam_policy" "lambda_policy" {
  for_each = { for key, value in var.lambda_function_list : value.function_name => value }

  name        = "${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-lambda-policy-${var.common.environment}"
  description = "Lambda Execution Policy"

  policy = jsonencode(
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "logs:CreateLogStream",
                    "logs:CreateLogGroup"
                ],
                "Resource": [
                    "arn:aws:logs:${var.common.aws_region}:${var.common.aws_account_id}:log-group:/aws/lambda/${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-${var.common.environment}*:*"
                ],
                "Effect": "Allow"
            },
            {
                "Action": [
                    "logs:PutLogEvents"
                ],
                "Resource": [
                    "arn:aws:logs:${var.common.aws_region}:${var.common.aws_account_id}:log-group:/aws/lambda/${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-${var.common.environment}*:*:*"
                ],
                "Effect": "Allow"
            },
            {
                "Action": [
                  "ec2:DescribeNetworkInterfaces",
                  "ec2:CreateNetworkInterface",
                  "ec2:DeleteNetworkInterface",
                  "ec2:DescribeInstances",
                  "ec2:AttachNetworkInterface"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }
  )
}

resource "aws_iam_role" "lambda-exec-role" {
  for_each = { for key, value in var.lambda_function_list : value.function_name => value }

  name = "${var.common.project_code}-${var.common.service_name}-${each.value.function_name}-lambda-role-${var.common.environment}"
  assume_role_policy = jsonencode(
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
  )

  tags = var.common.default_tags

}


resource "aws_iam_role_policy_attachment" "lambda-exec-role-policy-attachment" {
  for_each = { for key, value in var.lambda_function_list : value.function_name => value }

  role       = aws_iam_role.lambda-exec-role[each.value.function_name].name
  policy_arn = aws_iam_policy.lambda_policy[each.value.function_name].arn
}