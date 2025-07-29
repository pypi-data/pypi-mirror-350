import importlib
import json
import os
import shutil

import pkg_resources

from .utilities import replace_placeholders, to_terraform_hcl


class Generator:
    VARIABLE_MAPPING = {}  # Variable Mapping of module file template
    FOR_TERRAFORM_CONVERSION = []
    STAGED_MODULE_DETAILS = []
    REMOVED_MODULE_DETAILS = []

    def __init__(self, config):
        self.config = config

    @classmethod
    def assign_variables(cls, file, variables, required=True):
        return replace_placeholders(file, variables, required=required)

    @classmethod
    def create_file(cls, output_file, name_override=None):

        template_file = f"file_templates/{output_file}.txt"
        template_file = pkg_resources.resource_filename("terrayml", template_file)
        if not os.path.exists(template_file):
            print(f"❌ Error: Terraform template '{template_file}' not found.")
            return

        with open(template_file, "r") as file:
            template = file.read()

        terraform_code = replace_placeholders(
            template, cls.VARIABLE_MAPPING, required=True
        )

        generated_tf_folder_path = ".terraform"
        os.makedirs(generated_tf_folder_path, exist_ok=True)
        generated_tf_path = os.path.join(generated_tf_folder_path, output_file)
        if name_override:
            generated_tf_path = os.path.join(generated_tf_folder_path, name_override)

        with open(generated_tf_path, "w") as file:
            file.write(terraform_code)

        print(f"✅ Terraform file '{output_file}' generated successfully.")

    @classmethod
    def delete_file(cls, file):
        file_path = f".terraform/{file}"
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑️ Terraform file '{file}' removed successfully.")

    @classmethod
    def create_module(cls, module):
        source_module = f"modules/{module}"
        source_module = pkg_resources.resource_filename("terrayml", source_module)
        os.makedirs(".terraform/modules", exist_ok=True)
        destination_module = f".terraform/modules/{module}"
        shutil.copytree(
            source_module,
            destination_module,
            dirs_exist_ok=True,
            ignore=lambda src, names: [name for name in names if name == "__init__.py"],
        )
        print(f"✅ Terraform module '{module}' generated successfully.")

    @classmethod
    def delete_module(cls, module):
        os.makedirs(".terraform/modules", exist_ok=True)
        destination_module = f".terraform/modules/{module}"

        if os.path.exists(destination_module):
            shutil.rmtree(destination_module)
            print(f"🗑️ Terraform module '{module}' removed successfully.")

    @classmethod
    def create_object(cls, object_name, mapping={}):
        template_file = f"object_templates/{object_name}.json"
        template_file = pkg_resources.resource_filename("terrayml", template_file)
        with open(template_file, "r") as file:
            template = json.load(file)

        return replace_placeholders(template, mapping, required=True)

    @classmethod
    def copy_file(cls, file_path):
        source_path = pkg_resources.resource_filename("terrayml", file_path)
        shutil.copy(source_path, file_path)

    def stage_modules(self):
        for attr_name in dir(self):
            if attr_name.startswith("_stage"):
                method = getattr(self, attr_name)
                if callable(method) and not isinstance(method, classmethod):
                    method()

    def _stage_lambda_module(self):
        config = {
            "config_name": "lambda_functions",
            "object_name": "lambda_function",
            "file_template": "lambda_module",
            "module": "lambda",
            "object_list_variable": "LAMBDA_FUNCTIONS_LIST",
            "nested_module_config": [
                {
                    "config_name": "http",
                    "object_name": "api_gateway_lambda",
                    "file_template": "api_gateway_module",
                    "module": "api_gateway",
                    "object_list_variable": "LAMBDA_FUNCTIONS_WITH_APIGW_LIST",
                },
                {
                    "config_name": "event_bridge",
                    "object_name": "event_bridge_rule",
                    "file_template": "event_bridge_module",
                    "module": "event_bridge",
                    "object_list_variable": "EVENT_BRIDGE_RULE_LIST",
                },
                {
                    "config_name": "all_events",
                    "object_name": "lambda_event",
                    "file_template": "lambda_module",
                    "module": "lambda",
                    "object_list_variable": "LAMBDA_EVENTS_LIST",
                },
            ],
            "config_override_source": "LAMBDA_EVENTS_DICT",
        }
        self._simple_module_generation(**config)

    def _stage_api_gw_module(self):
        config = {
            "config_name": "api_gateways",
            "object_name": "api_gateway",
            "file_template": "api_gateway_module",
            "module": "api_gateway",
            "object_list_variable": "API_GATEWAY_LIST",
        }

        self._simple_module_generation(**config)

    def _stage_dynamodb_module(self):
        config = {
            "config_name": "dynamodb_tables",
            "object_name": "dynamodb_table",
            "file_template": "dynamodb_module",
            "module": "dynamodb",
            "object_list_variable": "DYNAMODB_LIST",
        }

        self._simple_module_generation(**config)

    def _stage_s3_module(self):
        config = {
            "config_name": "s3_buckets",
            "object_name": "s3_bucket",
            "file_template": "s3_module",
            "module": "s3",
            "object_list_variable": "S3_BUCKET_LIST",
        }

        self._simple_module_generation(**config)

    def _stage_vpc_module(self):
        config = {
            "config_name": "vpc",
            "object_name": "vpc",
            "file_template": "vpc_module",
            "module": "vpc",
            "object_list_variable": "VPC_LIST",
        }
        self._simple_module_generation(**config)

    def _stage_cognito_module(self):
        configs = [
            {
                "config_name": "cognito_user_pools",
                "object_name": "cognito_user_pool",
                "file_template": "cognito_module",
                "module": "cognito",
                "object_list_variable": "COGNITO_USER_POOL_LIST",
            },
            {
                "config_name": "cognito_identity_pools",
                "object_name": "cognito_identity_pool",
                "file_template": "cognito_module",
                "module": "cognito",
                "object_list_variable": "COGNITO_IDENTITY_POOL_LIST",
            },
        ]

        self._multi_source_module_generation(config_list=configs)

    def _stage_event_bridge_module(self):
        configs = [
            {
                "config_name": "event_bridge_buses",
                "object_name": "event_bridge_bus",
                "file_template": "event_bridge_module",
                "module": "event_bridge",
                "object_list_variable": "EVENT_BRIDGE_EVENT_BUS_LIST",
            },
            {
                "config_name": "event_bridge_rules",
                "object_name": "event_bridge_rule",
                "file_template": "event_bridge_module",
                "module": "event_bridge",
                "object_list_variable": "EVENT_BRIDGE_RULE_LIST",
            },
        ]

        self._multi_source_module_generation(config_list=configs)

    def _multi_source_module_generation(self, config_list):
        configs = config_list

        for index, config in enumerate(configs):
            self._simple_module_generation(
                config_name=config["config_name"],
                object_name=config["object_name"],
                file_template=config["file_template"],
                module=config["module"],
                object_list_variable=config["object_list_variable"],
                config_override=config.get("config_override", {}),
            )

    def _simple_module_generation(
        self,
        config_name,
        object_name,
        file_template,
        module,
        object_list_variable,
        config_override={},
        nested_module_config=[],
        config_override_source=None,
    ):

        config = self.config
        if config_override:
            config = config_override

        object_list = Generator.VARIABLE_MAPPING.get(object_list_variable, [])

        if config.get(config_name, None):

            mapping_module = importlib.import_module(
                f".mappings.{object_name}", package=__package__
            )

            for key, value in config.get(config_name, {}).items():
                variable_mapping = {}
                variable_mapping = mapping_module.generate_mappings(
                    key, value, Generator.VARIABLE_MAPPING
                )
                object_list.append(
                    Generator.create_object(object_name, variable_mapping)
                )

                if nested_module_config:
                    for config in nested_module_config:
                        config["config_override"] = variable_mapping[
                            config_override_source
                        ]
                    self._multi_source_module_generation(nested_module_config)

            Generator.FOR_TERRAFORM_CONVERSION.append(
                {f"{object_list_variable}": object_list}
            )

            Generator.STAGED_MODULE_DETAILS.append(
                {
                    "output_file": f"{file_template}.tf",
                    "module": module,
                }
            )
        else:
            Generator.REMOVED_MODULE_DETAILS.append(
                {
                    "output_file": f"{file_template}.tf",
                    "module": module,
                }
            )
        Generator.VARIABLE_MAPPING[object_list_variable] = object_list

    @classmethod
    def generate_terraform(cls):
        for for_conversion in Generator.FOR_TERRAFORM_CONVERSION:
            for key, value in for_conversion.items():
                Generator.VARIABLE_MAPPING[key] = to_terraform_hcl(value)

        for staged_module in Generator.STAGED_MODULE_DETAILS:
            Generator.create_file(output_file=staged_module["output_file"])
            Generator.create_module(staged_module["module"])

        for module_for_deletion in Generator.REMOVED_MODULE_DETAILS:
            if module_for_deletion not in Generator.STAGED_MODULE_DETAILS:
                Generator.delete_file(file=module_for_deletion["output_file"])
                Generator.delete_module(module_for_deletion["module"])
