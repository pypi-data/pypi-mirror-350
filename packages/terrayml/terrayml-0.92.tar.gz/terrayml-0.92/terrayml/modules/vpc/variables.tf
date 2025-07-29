variable "common" {
  description = "common variables"
}

variable "vpc_list" {
  type = list(object({
    vpc_name = string
    cidr_block = string
    subnets = list(object({
      subnet_name = string
      subnet_cidr_block = string
      availability_zone = string
    }))
    internet_gateways = list(string)
    nat_gateways = list(object({
      nat_gateway_name = string
      subnet = string
    }))
    route_tables = list(object({
      route_table_name = string
      subnets = list(string)
      routes = list(object({
        destination_cidr_block = string
        target_type = string
        target = string
      }))
    }))
    vpc_endpoints = list(object({
      endpoint_name = string
      endpoint_type = string
      endpoint_service = string
      route_tables = list(string)
    }))
    # nat_gateway = list()
  }))
  description = "vpc list"
}