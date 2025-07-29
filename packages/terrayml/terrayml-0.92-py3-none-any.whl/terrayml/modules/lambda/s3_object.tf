resource "aws_s3_bucket" "lambda_s3" {
  bucket = "${lower(var.common.project_code)}-${var.service_name}-${var.common.environment}-lambda-deploymentbucket"
  tags = var.common.default_tags
}

data "archive_file" "this" {
  type = "zip"

  source_dir  = "${var.app_path}/app"
  output_path = "${var.app_path}/.tftemp/${var.service_name}.zip"
}

resource "aws_s3_object" "this" {
  bucket                 = aws_s3_bucket.lambda_s3.bucket
  key                    = "lambda/${var.common.project_code}-${var.service_name}-${var.common.environment}-lambda.zip"
  source                 = "${var.app_path}/.tftemp/${var.service_name}.zip"
  source_hash            = data.archive_file.this.output_md5

  tags = var.common.default_tags

}