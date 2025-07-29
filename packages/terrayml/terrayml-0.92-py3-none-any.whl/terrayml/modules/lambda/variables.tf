variable "common" {
  description = "common variables"
}
variable "service_name" {
  description = "service name"
}

variable "runtime" {
  type = string
}

variable "apigw_execution_arns" {
  type = map(string)
}

variable "app_path" {
  type = string
}

variable "lambda_events_list" {
 type = list(object({
      function_name = string
      event_type = string
      event_details = object({
        # http
        rule_name = optional(string)
        path = optional(string)
        method = optional(string)
        api_gateway = optional(string)
        
        # event_bridge
        event_bus = optional(string)
        pattern = optional(object({
          source = list(string)
          detail_type = list(string)
        }))
        execution_arn = optional(string)
        target_arn = optional(string)

        # cognito_user_pool
        cognito_arn = optional(string)
        trigger_type = optional(string)
        trigger_config = optional(object({
          lambda_version = string
        }))
      })
    }))
  description = "lambda events"
}
variable "lambda_function_list" {
  type = list(object({
    service_name = string
    function_name = string
    description = string
    role = string
    handler = string
    runtime = string
    memory_size = number
    timeout = number
    custom_layers = list(string)
    vpc_config = map(list(string))
    variables = map(string)
    explicit_service_policies = list(object({
      service_name = string
      allowed_actions = list(string)
      allowed_resources = list(string)
    }))
  }))
  description = "Lambda Function List"
}