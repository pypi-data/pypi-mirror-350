variable "common" {
  description = "common variables"
}

variable "api_gateway_list" {
  type = list(object({
    api_gateway_name = string
    authorizers = list(object({
      authorizer_name = string
      authorizer_type = string
      authorizer_provider_arns = list(string)
      authorizer_identity_source = string
    }))
  }))
  description = "API GW List"
}

variable "api_gateway_lambda_list" {
  type = list(object({
    function_name = string
    api_gateway_name = string
    path = string
    method = string
    invoke_arn = string
    authorizer_type = string
    authorizer_name = string
    authorization_scopes = list(string)
  }))
  description = "API GW Lambda List"
}