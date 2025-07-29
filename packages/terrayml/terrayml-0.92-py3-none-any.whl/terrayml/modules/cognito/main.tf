locals {
  cognito_clients = flatten([
    for user_pool_key, user_pool in var.cognito_user_pool_list: [
      for client_key, client in user_pool.clients: {
        user_pool_key = user_pool_key
        user_pool_name = user_pool.name
        client_key = client_key
        client_name = client.name
        user_pool_id = aws_cognito_user_pool.this[user_pool.name].id
        domain_name = user_pool.domain_name
        prevent_user_existence_errors  = client.prevent_user_existence_errors
        access_token_validity  = client.access_token_validity
        id_token_validity      = client.id_token_validity
        refresh_token_validity = client.refresh_token_validity

        supported_identity_providers = client.supported_identity_providers
        generate_secret = client.generate_secret
        explicit_auth_flows = client.explicit_auth_flows
        allowed_oauth_flows = client.allowed_oauth_flows
        allowed_oauth_scopes = client.allowed_oauth_scopes
        allowed_oauth_flows_user_pool_client = client.allowed_oauth_flows_user_pool_client
        callback_urls = client.callback_urls
        logout_urls = client.logout_urls
      }
    ]
  ])
  cognito_groups = flatten([
    for user_pool_key, user_pool in var.cognito_user_pool_list: [
      for group_key, group in user_pool.groups: {
        user_pool_key = user_pool_key
        user_pool_name = user_pool.name
        user_pool_id = aws_cognito_user_pool.this[user_pool.name].id

        group_key = group_key
        group_name = group.name
        group_description = group.description
        group_precedence = group.precedence
      }
    ]
  ])

  resource_servers = flatten([
    for user_pool_key, user_pool in var.cognito_user_pool_list: [
      for resource_server_key, resource_server in user_pool.resource_servers: {
        user_pool_key = user_pool_key
        user_pool_name = user_pool.name
        user_pool_id = aws_cognito_user_pool.this[user_pool.name].id
        resource_server_key = resource_server_key
        resource_server_identifier = resource_server.identifier
        resource_server_name = resource_server.name
        resource_server_scopes = resource_server.scopes
        
      }
    ]
  ])
}

resource "aws_cognito_user_pool" "this" {
  for_each      = { for key, value in var.cognito_user_pool_list : value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}"
  admin_create_user_config {
    allow_admin_create_user_only = each.value.allow_admin_create_user_only == "TRUE" ? true : false
  }
  alias_attributes         = length(each.value.alias_attributes) > 0 ? each.value.alias_attributes : null
  username_attributes      = length(each.value.username_attributes) > 0 ? each.value.username_attributes : null
  auto_verified_attributes = each.value.auto_verified_attributes
  deletion_protection      = each.value.deletion_protection == "TRUE"? "ACTIVE" : "INACTIVE"
  device_configuration {
    challenge_required_on_new_device      = each.value.device_configuration.challenge_required_on_new_device == "TRUE" ? true : false
    device_only_remembered_on_user_prompt = each.value.device_configuration.device_only_remembered_on_user_prompt == "TRUE" ? true : false
  }
  mfa_configuration = each.value.mfa_configuration
  software_token_mfa_configuration {
    enabled = each.value.software_token_mfa_configuration_is_enabled == "TRUE" ? true : false
  }
  password_policy {
    minimum_length                   = each.value.password_policy.minimum_length
    require_lowercase                = each.value.password_policy.require_lowercase == "TRUE" ? true : false
    require_numbers                  = each.value.password_policy.require_numbers == "TRUE" ? true: false
    require_symbols                  = each.value.password_policy.require_symbols == "TRUE" ? true : false
    require_uppercase                = each.value.password_policy.require_uppercase == "TRUE" ? true : false
    temporary_password_validity_days = each.value.password_policy.temporary_password_validity_days
  }
  dynamic "schema" {
    for_each = each.value.attributes
    content {
      name                = schema.value.name
      attribute_data_type = schema.value.attribute_data_type
      required            = schema.value.required == "TRUE" ? true : false
      mutable             = schema.value.mutable == "TRUE" ? true : false
      dynamic "string_attribute_constraints" {
        for_each = schema.value.attribute_data_type == "String" && schema.value.constraints != {} ? [schema.value.constraints] : []
        content {
          min_length = string_attribute_constraints.value.min_length
          max_length = string_attribute_constraints.value.max_length
        }
      }
      dynamic "number_attribute_constraints" {
        for_each = schema.value.attribute_data_type == "Number" && schema.value.constraints != {} ? [schema.value.constraints] : []
        content {
          min_value = number_attribute_constraints.value.min_value
          max_value = number_attribute_constraints.value.max_value
        }
      }
    }
  }

  tags = var.common.default_tags 
   
  lifecycle {
    ignore_changes = [
      lambda_config, schema
    ]
  }

}
resource "aws_cognito_user_group" "this" {
  for_each = tomap({
    for group in local.cognito_groups: "${group.user_pool_name}.${group.group_name}" => group
  })
  name         = each.value.group_name
  user_pool_id = each.value.user_pool_id
  description  = each.value.group_description
  precedence   = each.value.group_precedence != "NONE" ? each.value.group_precedence : null
}

resource "aws_cognito_resource_server" "this" {
  for_each = tomap({
    for resource_server in local.resource_servers: "${resource_server.user_pool_name}.${resource_server.resource_server_name}" => resource_server
  })
  user_pool_id = each.value.user_pool_id
  identifier   = each.value.resource_server_identifier
  name         = each.value.resource_server_name

  dynamic "scope" {
    for_each = each.value.resource_server_scopes
    content {
      scope_name        = scope.value.scope_name
      scope_description = scope.value.scope_description
    }
  }
}

resource "aws_cognito_user_pool_client" "this" {
  for_each = tomap({
    for client in local.cognito_clients: "${client.user_pool_name}.${client.client_name}" => client
  })
  name         = "${var.common.project_code}-${var.common.environment}-${each.value.client_name}"
  user_pool_id = each.value.user_pool_id
  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }
  prevent_user_existence_errors = each.value.prevent_user_existence_errors == "TRUE" ? "ENABLED" : null
  access_token_validity  = each.value.access_token_validity
  id_token_validity      = each.value.id_token_validity
  refresh_token_validity = each.value.refresh_token_validity

  supported_identity_providers         = each.value.supported_identity_providers
  generate_secret                      = each.value.generate_secret == "TRUE" ? true : false
  explicit_auth_flows                  = each.value.explicit_auth_flows
  allowed_oauth_flows                  = each.value.allowed_oauth_flows
  allowed_oauth_scopes                 = each.value.allowed_oauth_scopes
  allowed_oauth_flows_user_pool_client = each.value.allowed_oauth_flows_user_pool_client == "TRUE" ? true : false
  callback_urls                        = each.value.callback_urls
  logout_urls                          = each.value.logout_urls

  depends_on = [ aws_cognito_resource_server.this ]
}


resource "aws_cognito_identity_pool" "this" {
  for_each = { for key, value in var.cognito_identity_pool_list: value.name => value }

  identity_pool_name               = "${var.common.project_code}-${var.common.environment}-${each.value.name}"
  allow_unauthenticated_identities = each.value.allow_unauthenticated_identities == "TRUE" ? true : false

  dynamic "cognito_identity_providers" {
    for_each = each.value.cognito_identity_providers_list
    content {
      client_id               = aws_cognito_user_pool_client.this["${cognito_identity_providers.value.user_pool_name}.${cognito_identity_providers.value.client_name}"].id
      provider_name           = "cognito-idp.${var.common.aws_region}.amazonaws.com/${aws_cognito_user_pool.this[cognito_identity_providers.value.user_pool_name].id}"
      server_side_token_check = cognito_identity_providers.value.server_side_token_check == "TRUE" ? true : false
    }
  }

  # supported_login_providers = {
  #   "graph.facebook.com"  = "7346241598935552"
  #   "accounts.google.com" = "123456789012.apps.googleusercontent.com"
  # }

  # saml_provider_arns           = [aws_iam_saml_provider.default.arn]
  # openid_connect_provider_arns = ["arn:aws:iam::123456789012:oidc-provider/id.example.com"]

  tags = var.common.default_tags
}

resource "aws_cognito_user_pool_domain" "this" {
  for_each      = { for key, value in var.cognito_user_pool_list : value.name => value }
  domain       = "${each.value.domain_name}-${var.common.environment}"
  user_pool_id = aws_cognito_user_pool.this[each.value.name].id
}

resource "aws_iam_role" "authenticated_role" {
  for_each = { for key, value in var.cognito_identity_pool_list: value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-authenticated-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = "cognito-identity.amazonaws.com"
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "cognito-identity.amazonaws.com:aud" = aws_cognito_identity_pool.this[each.value.name].id
          },
          "ForAnyValue:StringLike" = {
            "cognito-identity.amazonaws.com:amr" = "authenticated"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "authenticated_policy" {
  for_each = { for key, value in var.cognito_identity_pool_list: value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-authenticated-policy"
  role = aws_iam_role.authenticated_role[each.value.name].name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "mobileanalytics:PutEvents",
          "cognito-sync:*",
          "cognito-identity:*",
        ],
        Resource = "*",
      },
      {
        Effect   = "Allow",
        Action   = "s3:*",
        Resource = "*",
      },
    ]
  })
}

resource "aws_cognito_identity_pool_roles_attachment" "admin_identity_pool_role_mapping" {
  for_each = { for key, value in var.cognito_identity_pool_list: value.name => value }
  identity_pool_id = aws_cognito_identity_pool.this[each.value.name].id
  roles = {
    authenticated = aws_iam_role.authenticated_role[each.value.name].arn
  }
}

output "cognito_user_pool_arns" {
  value = { for key, value in var.cognito_user_pool_list : value.name => aws_cognito_user_pool.this[value.name].arn }
}