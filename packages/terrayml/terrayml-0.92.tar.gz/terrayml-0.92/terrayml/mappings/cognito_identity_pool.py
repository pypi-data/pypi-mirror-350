def generate_mappings(config_key, config_value, other_reference_mappings):
    return {
        "COGNITO_IDENTITY_POOL_NAME": config_key,
        "COGNITO_IDENTITY_POOL_ALLOW_UNAUTH_IDS": str(
            config_value.get("allow_unauthenticated_identities", True)
        ).upper(),
        "COGNITO_IDENTITY_POOL_IDPS": [
            {
                "user_pool_name": identity_provider["user_pool_name"],
                "client_name": identity_provider["client_name"],
                "server_side_token_check": str(
                    identity_provider.get("server_side_token_check", False)
                ).upper(),
            }
            for identity_provider in config_value.get("cognito_identity_providers", [])
        ],
    }
