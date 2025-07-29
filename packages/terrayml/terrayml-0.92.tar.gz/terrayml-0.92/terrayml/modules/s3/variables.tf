variable "common" {
  description = "common variables"
}

variable "s3_bucket_list" {
  type = list(object({
    bucket_name = string
  }))
  description = "s3 bucket list"
}