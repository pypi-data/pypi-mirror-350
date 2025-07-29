variable "common" {
  description = "common variables"
}
variable "event_bridge_rule_list" {
  type = list(object({
    event_bridge_rule_name = string
    event_bridge_rule_source = list(string)
    event_bridge_rule_detail_type = list(string)
    event_bridge_rule_target_arn = string
    event_bridge_rule_target_bus_name = string
  }))
  description = "Event Bridge Rule list"
}
variable "event_bridge_event_bus_list" {
  type = list(object({
    event_bridge_bus_name = string
    event_bridge_bus_description = string
  }))
  description = "Event Bridge Rule list"
}