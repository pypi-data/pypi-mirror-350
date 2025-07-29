def generate_mappings(config_key, config_value, other_reference_mappings):
    return {
        "COGNITO_USER_POOL_NAME": config_key,
        "COGNITO_USER_POOL_DOMAIN_NAME": config_value["domain_name"],
        "COGNITO_ALLOW_ADMIN_CREATE_USER_ONLY": str(
            config_value.get("allow_admin_create_user_only", False)
        ).upper(),
        "COGNITO_ALIAS_ATTRIBUTES": config_value.get("alias_attributes", []),
        "COGNITO_USERNAME_ATTRIBUTES": config_value.get("username_attributes", []),
        "COGNITO_AUTO_VERIFIED_ATTRIBUTES": config_value["auto_verified_attributes"],
        "COGNITO_ATTRIBUTES": [
            {
                "name": key,
                "attribute_data_type": str(value["data_type"]).capitalize(),
                "required": str(value.get("required", True)).upper(),
                "mutable": str(value.get("mutable", True)).upper(),
                "constraints": value.get("constraints", {}),
            }
            for key, value in config_value.get("attributes", {}).items()
        ],
        "COGNITO_DELETION_PROTECTION": str(
            config_value.get("deletion_protection", False)
        ).upper(),
        "COGNITO_DEVICE_CONFIGURATION": {
            "challenge_required_on_new_device": str(
                config_value.get("device_configuration", {}).get(
                    "challenge_required_on_new_device", False
                )
            ).upper(),
            "device_only_remembered_on_user_prompt": str(
                config_value.get("device_configuration", {}).get(
                    "device_only_remembered_on_user_prompt", False
                )
            ).upper(),
        },
        "COGNITO_MFA_CONFIGURATION": config_value.get("mfa_configuration", "OPTIONAL"),
        "COGNITO_SOFTWARE_TOKEN_MFA_ENABLE": str(
            config_value.get("software_token_mfa_configuration_is_enabled", False)
        ).upper(),
        "COGNITO_PASSWORD_POLICY": {
            "minimum_length": config_value.get("password_policy", {}).get(
                "minimum_length", 12
            ),
            "require_lowercase": str(
                config_value.get("password_policy", {}).get("require_lowercase", True)
            ).upper(),
            "require_numbers": str(
                config_value.get("password_policy", {}).get("require_numbers", True)
            ).upper(),
            "require_symbols": str(
                config_value.get("password_policy", {}).get("require_symbols", True)
            ).upper(),
            "require_uppercase": str(
                config_value.get("password_policy", {}).get("require_uppercase", True)
            ).upper(),
            "temporary_password_validity_days": config_value.get(
                "password_policy", {}
            ).get("temporary_password_validity_days", 3),
        },
        "COGNITO_CLIENTS": [
            {
                "name": key,
                "prevent_user_existence_errors": str(
                    value.get("prevent_user_existence_errors", True)
                ).upper(),
                "access_token_validity": value.get("access_token_validity", 60),
                "id_token_validity": value.get("id_token_validity", 60),
                "refresh_token_validity": value.get("refresh_token_validity", 30),
                "generate_secret": str(value.get("generate_secret", False)).upper(),
                "supported_identity_providers": value.get(
                    "supported_identity_providers", ["COGNITO"]
                ),
                "explicit_auth_flows": value.get(
                    "explicit_auth_flows",
                    [
                        "ALLOW_USER_PASSWORD_AUTH",
                        "ALLOW_REFRESH_TOKEN_AUTH",
                        "ALLOW_USER_SRP_AUTH",
                    ],
                ),
                "allowed_oauth_flows_user_pool_client": str(
                    value.get("allowed_oauth_flows_user_pool_client", True)
                ).upper(),
                "allowed_oauth_flows": value.get(
                    "allowed_oauth_flows",
                    ["code"],
                ),
                "allowed_oauth_scopes": value.get(
                    "allowed_oauth_scopes",
                    ["openid", "email", "aws.cognito.signin.user.admin"],
                ),
                "callback_urls": value.get(
                    "callback_urls",
                    ["http://localhost:3000/signin"],
                ),
                "logout_urls": value.get(
                    "logout_urls",
                    ["http://localhost:3000/logout"],
                ),
            }
            for key, value in config_value.get("clients", {}).items()
        ],
        "COGNITO_RESOURCE_SERVERS": [
            {
                "name": key,
                "identifier": value["identifier"],
                "scopes": value["scopes"],
            }
            for key, value in config_value.get("resource_servers", {}).items()
        ],
        "COGNITO_GROUPS": [
            {
                "name": key,
                "description": value["description"],
                "precedence": value.get("precedence", "NONE"),
            }
            for key, value in config_value.get("groups", {}).items()
        ],
    }
