resource "aws_s3_bucket" "this" {
    for_each    = { for key, value in var.s3_bucket_list : value.bucket_name => value }
    bucket      = lower("${var.common.project_code}-${var.common.environment}-${each.value.bucket_name}")
    tags        = var.common.default_tags
}