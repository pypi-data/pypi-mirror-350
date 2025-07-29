import os
import re


def replace_placeholders(data, mapping=None, required=True):
    """
    Recursively replace placeholders in data.
    Supports nested keys when the placeholder name includes dots.
    If a placeholder starts with "var.", it is left unchanged.
    """
    if mapping is None:
        mapping = {}

    def get_value(var_name):
        # This function is only called for placeholders that don't start with "var."
        if "." in var_name:
            parts = var_name.split(".")
            value = mapping
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = None
                    break
            if value is None and required:
                raise ValueError(f"❌ Error: Missing required variable '{var_name}'.")
            return value
        else:
            value = mapping.get(var_name, os.getenv(var_name))
            if value is None and required:
                raise ValueError(f"❌ Error: Missing required variable '{var_name}'.")
            return value

    if isinstance(data, str):
        # Check if the entire string is an exact placeholder.
        exact_match = re.fullmatch(r"\$\{([^}]+)\}", data)
        if exact_match:
            var_name = exact_match.group(1)
            # If it's a Terraform variable reference, leave it unchanged.
            if var_name.startswith("var.") or var_name.startswith("local."):
                return data
            return get_value(var_name)

        # Otherwise, replace all occurrences.
        def replacer(match):
            var_name = match.group(1)
            if var_name.startswith("var.") or var_name.startswith("local."):
                return match.group(
                    0
                )  # Leave the Terraform variable reference unchanged.
            return str(get_value(var_name))

        return re.sub(r"\$\{([^}]+)\}", replacer, data)
    elif isinstance(data, dict):
        return {
            key: replace_placeholders(value, mapping, required)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [replace_placeholders(item, mapping, required) for item in data]
    return data


def to_terraform_hcl(data, indent=2):
    """
    Convert a Python data structure into Terraform HCL format.
    All string values are wrapped in quotes.
    """

    def format_value(value, level=0):
        spacing = " " * (level * indent)
        if isinstance(value, dict):
            lines = ["{"]
            for key, val in value.items():
                lines.append(f"{spacing}  {key} = {format_value(val, level+1)}")
            lines.append(spacing + "}")
            return "\n".join(lines)
        elif isinstance(value, list):
            # For lists of dicts, pretty-print each item.
            if all(isinstance(item, dict) for item in value):
                lines = ["["]
                for item in value:
                    lines.append(f"{spacing}  {format_value(item, level+1)},")
                lines.append(spacing + "]")
                return "\n".join(lines)
            else:
                items = [format_value(item, level) for item in value]
                return "[ " + ", ".join(items) + " ]"
        elif isinstance(value, str):
            if value.startswith("module."):
                return value
            else:
                return f'"{value}"'
        else:
            return str(value)

    return format_value(data)
