def generate_mappings(config_key, config_value, other_reference_mappings):

    return {
        "LAMBDA_FUNCTION_NAME": config_value["function_name"],
        "LAMBDA_EVENT_TYPE": config_value["event_type"],
        "LAMBDA_EVENT_DETAILS": config_value["event_details"],
    }
