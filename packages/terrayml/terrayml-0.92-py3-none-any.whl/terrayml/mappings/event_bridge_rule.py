def generate_mappings(config_key, config_value, other_reference_mappings):
    return {
        "EVENT_BRIDGE_RULE_NAME": config_value["rule_name"],
        "EVENT_BRIDGE_RULE_SOURCE": config_value["pattern"]["source"],
        "EVENT_BRIDGE_RULE_DETAIL_TYPE": config_value["pattern"]["detail_type"],
        "EVENT_BRIDGE_RULE_TARGET_ARN": config_value["target_arn"],
        "EVENT_BRIDGE_RULE_TARGET_BUS_NAME": config_value["event_bus"],
    }
