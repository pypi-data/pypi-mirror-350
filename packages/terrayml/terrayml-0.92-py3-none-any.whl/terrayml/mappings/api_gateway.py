def generate_mappings(config_key, config_value, other_reference_mappings):
    config_value = config_value or {}

    return {
        "API_GATEWAY_NAME": config_key,
        "API_GATEWAY_AUTHORIZERS": [
            {
                "authorizer_name": authorizer["name"],
                "authorizer_type": authorizer["type"],
                "authorizer_provider_arns": authorizer["provider_arns"],
                "authorizer_identity_source": authorizer["identity_source"],
            }
            for authorizer in config_value.get("authorizers", [])
        ],
    }
