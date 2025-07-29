def generate_mappings(config_key, config_value, other_reference_mappings):
    return {
        "DYNAMODB_TABLE_NAME": config_key,
        "DYNAMODB_HASH_KEY": config_value["hash_key"],
        "DYNAMODB_RANGE_KEY": config_value.get("range_key", "NONE"),
        "DYNAMODB_ATTRIBUTES": [
            {"name": key, "type": value}
            for key, value in config_value["attributes"].items()
        ],
        "DYNAMODB_GLOBAL_SECONDARY_INDEXES": [
            {
                "name": key,
                "hash_key": value["hash_key"],
                "range_key": value["range_key"],
                "projection_type": value["projection_type"],
            }
            for key, value in config_value.get("global_secondary_indexes", {}).items()
        ],
        "DYNAMODB_LOCAL_SECONDARY_INDEXES": [
            {
                "name": key,
                "range_key": value["range_key"],
                "projection_type": value["projection_type"],
            }
            for key, value in config_value.get("local_secondary_indexes", {}).items()
        ],
    }
