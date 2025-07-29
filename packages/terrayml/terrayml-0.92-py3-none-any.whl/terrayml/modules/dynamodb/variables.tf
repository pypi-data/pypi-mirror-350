variable "common" {
  description = "common variables"
}

variable "dynamodb_list" {
  type = list(object({
    table_name = string
    hash_key = string
    range_key = string
    attributes = list(object({
      name = string
      type = string
    }))
    global_secondary_indexes = list(object({
      name = string
      hash_key = string
      range_key = string
      projection_type = string
    }))
    local_secondary_indexes = list(object({
      name = string
      range_key = string
      projection_type = string
    }))
  }))
  description = "Dynamodb table"
}