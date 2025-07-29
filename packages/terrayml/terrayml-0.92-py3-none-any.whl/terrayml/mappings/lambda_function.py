def generate_mappings(config_key, config_value, other_reference_mappings):

    mapping = {
        "LAMBDA_SERVICE_NAME": other_reference_mappings["SERVICE_NAME"],
        "LAMBDA_FUNCTION_NAME": config_key,
        "LAMBDA_FUNCTION_DESCRIPTION": config_value.get("description", ""),
        "LAMBDA_HANDLER": config_value["handler"],
        "LAMBDA_RUNTIME": config_value.get("runtime", "python3.11"),
        "LAMBDA_MEMORY_SIZE": config_value.get("memory_size", 128),
        "LAMBDA_TIMEOUT": config_value.get("timeout", 30),
        "LAMBDA_CUSTOM_LAYERS": config_value.get("custom_layer_arns", []),
        "LAMBDA_VPC_SUBNET_IDS": config_value.get("subnet_ids", []),
        "LAMBDA_VPC_SECURITY_GROUP_IDS": config_value.get("security_group_ids", []),
        "LAMBDA_VARIABLES": config_value.get("variables", {}),
        "LAMBDA_EXPLICIT_SERVICE_POLICIES": [
            {
                "service_name": key,
                "allowed_actions": value["allowed_actions"],
                "allowed_resources": value["allowed_resources"],
            }
            for key, value in config_value.get("explicit_service_policies", {}).items()
        ],
    }

    mapping["LAMBDA_EVENTS_DICT"] = {}
    mapping["LAMBDA_EVENTS_DICT"]["all_events"] = {}

    for event in config_value.get("events", []):
        for event_type, event_details in event.items():
            event_details["rule_name"] = f"{config_key}-{event_type}"

            if event_type == "event_bridge":
                event_details["execution_arn"] = (
                    f"module.event_bridge.execution_rule_arns[\"{event_details['rule_name']}\"]"
                )
                event_details["target_arn"] = (
                    f'module.lambda_functions.lambda_arns["{config_key}"]'
                )
            event_object = {
                "function_name": config_key,
                "event_type": event_type,
                "event_details": event_details,
            }
            mapping["LAMBDA_EVENTS_DICT"][event_type] = {f"{config_key}": event_details}
            mapping["LAMBDA_EVENTS_DICT"]["all_events"][event_type] = event_object

    return mapping
