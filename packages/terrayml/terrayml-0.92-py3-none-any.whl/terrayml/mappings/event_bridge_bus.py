def generate_mappings(config_key, config_value, other_reference_mappings):
    return {
        "EVENT_BRIDGE_BUS_NAME": config_key,
        "EVENT_BRIDGE_BUS_DESCRIPTION": config_value["description"],
    }
