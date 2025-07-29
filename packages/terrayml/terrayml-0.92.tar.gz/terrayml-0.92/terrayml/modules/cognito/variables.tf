variable "common" {
  description = "common variables"
}

variable "cognito_user_pool_list" {
  type = list(object({
    name = string
    domain_name = string
    allow_admin_create_user_only = string
    alias_attributes = list(string)
    username_attributes = list(string)
    auto_verified_attributes = list(string)
    deletion_protection = string
    device_configuration = object({
      challenge_required_on_new_device = string
      device_only_remembered_on_user_prompt = string
    })
    mfa_configuration = string
    software_token_mfa_configuration_is_enabled = string
    password_policy = object({
      minimum_length = number
      require_lowercase = string
      require_numbers = string
      require_symbols = string
      require_uppercase = string
      temporary_password_validity_days = number
    })
    attributes = list(object({
      name = string
      attribute_data_type = string
      required = string
      mutable = string
      constraints = object({
        min_length = optional(number)
        max_length = optional(number)
        
        min_value = optional(number)
        max_value = optional(number)
      })
    }))
    groups = list(object({
      name = string
      description = string
      precedence = string
    }))
    clients = list(object({
      name = string
      prevent_user_existence_errors = string
      access_token_validity = number
      id_token_validity = number
      refresh_token_validity = number
      generate_secret = string
      supported_identity_providers = list(string)
      explicit_auth_flows = list(string)
      allowed_oauth_flows = list(string)
      allowed_oauth_scopes = list(string)
      allowed_oauth_flows_user_pool_client = string
      callback_urls = list(string)
      logout_urls = list(string)
    }))
    resource_servers = list(object({
      identifier = string
      name = string
      scopes = list(object({
        scope_name = string
        scope_description = string
      }))
    }))
  }))
  description = "Cognito User Pool"
}

variable "cognito_identity_pool_list" {
  type = list(object({
    name = string
    allow_unauthenticated_identities = string
    cognito_identity_providers_list = list(object({
      user_pool_name = string
      client_name = string
      server_side_token_check = string
    }))
  }))
  description = "Cognito Identity Pool"
}