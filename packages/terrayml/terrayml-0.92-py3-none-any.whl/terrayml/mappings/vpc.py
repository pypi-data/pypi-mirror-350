def generate_mappings(config_key, config_value, other_reference_mappings):
    mapping = {
        "VPC_NAME": config_key,
        "VPC_CIDR_BLOCK": config_value["cidr-block"],
        "VPC_SUBNETS": [
            {
                "subnet_name": key,
                "subnet_cidr_block": value.get("cidr-block", {}),
                "availability_zone": value.get("availability-zone", {}),
            }
            for key, value in config_value.get("subnets", {}).items()
        ],
        "VPC_ENDPOINTS": [
            {
                "endpoint_name": key,
                "endpoint_type": value["endpoint_type"],
                "endpoint_service": value["service_code"],
                "route_tables": value["route_tables"],
            }
            for key, value in config_value.get("vpc-endpoints", {}).items()
        ],
        "VPC_NAT_GATEWAYS": [
            {
                "nat_gateway_name": key,
                "subnet": value["subnet"],
            }
            for key, value in config_value.get("nat-gateways", {}).items()
        ],
        "VPC_INTERNET_GATEWAYS": config_value.get("internet-gateways", []),
        "VPC_ROUTE_TABLES": [
            {
                "route_table_name": key,
                "subnets": value.get("subnets", {}),
                "routes": value.get("routes", []),
            }
            for key, value in config_value.get("route-tables", {}).items()
        ],
    }
    return mapping
