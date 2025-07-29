def generate_mappings(config_key, config_value, other_reference_mappings):
    return {
        "LAMBDA_FUNCTION_NAME": config_key,
        "LAMBDA_API_GATEWAY_NAME": config_value["api_gateway"],
        "LAMBDA_PATH": config_value["path"],
        "LAMBDA_METHOD": config_value["method"],
        "LAMBDA_AUTHORIZATION_TYPE": config_value.get("authorizer", {}).get(
            "type", "NONE"
        ),
        "LAMBDA_AUTHORIZATION_NAME": config_value.get("authorizer", {}).get(
            "name", "NONE"
        ),
        "LAMBDA_AUTHORIZATION_SCOPES": config_value.get("authorizer", {}).get(
            "scopes", []
        ),
    }
