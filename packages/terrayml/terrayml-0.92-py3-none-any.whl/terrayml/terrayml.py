import os
import shutil
import subprocess
import sys

import click

from .generator import Generator
from .loader import load_env_file, load_yaml

DEFAULT_YAML_FILE = "terrayml.yml"


def generate_terraform(yaml_file, backend_type):
    """Generate Terraform file based on updated YAML configuration."""
    # yaml_file = yaml_file or DEFAULT_YAML_FILE  # Use default YAML if none specified

    try:
        os.makedirs(".tftemp", exist_ok=True)
        Generator.copy_file(file_path=".env.example")

        if not os.path.exists(yaml_file):
            raise FileNotFoundError(
                f"❌ Error: Target Terrayml Config file '{yaml_file}' not found."
            )
        if not os.path.exists("requirements.txt"):
            raise FileNotFoundError(f"❌ Error: requirements.txt file not found.")

        print(f"📄 Using YAML file: {yaml_file}")
        config = load_yaml(yaml_file)
        environment = config["environment"]
        load_env_file(environment)

        updated_config = Generator.assign_variables(config, os.environ)

        Generator.VARIABLE_MAPPING = {
            "AWS_REGION": updated_config["provider"]["region"],
            "PROJECT_NAME": updated_config["project_name"],
            "PROJECT_CODE": updated_config["project_code"],
            "TERRAYML_RUNTIME": updated_config["runtime"],
            "LOWERED_PROJECT_CODE": updated_config["project_code"].lower(),
            "SERVICE_NAME": updated_config["service_name"],
            "AWS_ACCOUNT_ID": os.environ["AWS_ACCOUNT_ID"],
            "AWS_PROFILE": os.environ["AWS_PROFILE"],
            "TERRAYML_PATH": os.getcwd(),
            "ENVIRONMENT": environment,
        }

        if backend_type == "remote":
            Generator.create_file(output_file="main.tf")
        elif backend_type == "local":
            Generator.create_file(
                output_file="backend_main.tf", name_override="main.tf"
            )
        Generator.create_file(output_file="terraform.tfvars")
        Generator.create_file(output_file="variables.tf")

        generator = Generator(updated_config)
        generator.stage_modules()
        generator.generate_terraform()

    except FileNotFoundError as e:
        print(str(e))
        print("❌ Terraform generation failed due to missing file.")
    except ValueError as e:
        print(str(e))
        print(
            "❌ Terraform generation failed due to missing variables. Fix the missing variables and try again."
        )
    except Exception as e:
        print(str(e))
        print("❌ Terraform generation failed due to unknown error.")


@click.group()
def cli():
    """Terrayml - Terraform Generator from YAML"""
    pass


@click.command()
@click.option(
    "--yaml_file",
    default=DEFAULT_YAML_FILE,
    help="Your terrayml.yml format file. Defaults to terrayml.yml",
)
@click.option(
    "--backend_type",
    default="remote",
    help="This indicates that you are generating a remote backend terraform code base. Other option is 'local'.",
)
def generate(yaml_file, backend_type):
    """Generate Terraform files from a YAML file with environment variables."""
    if shutil.which("zip") is None:
        print(
            "❌ Error: 'zip' is required. Please install it using 'sudo apt install zip' and try again."
        )
        return None
    generate_terraform(yaml_file, backend_type)


@click.command()
@click.option(
    "--aws_profile",
    default="default",
    help="Your AWS profile in .aws/credentials.",
)
@click.option(
    "--aws_region",
    default="us-east-1",
    help="Your AWS region.",
)
def local_api(aws_profile, aws_region):
    """Change directory to .terraform and run terraform init."""
    terrayml_path = os.path.join(os.getcwd(), ".terraform")

    click.echo(
        f"Changing directory to {terrayml_path} and running SAM cli command to start local api..."
    )

    if not os.path.isdir(terrayml_path):
        click.echo("Error: .terraform directory does not exist!")
        return

    click.echo(f"Running nodemon to watch on app folder")
    nodemon_process = subprocess.Popen(
        [
            "nodemon",
            "--watch",
            "app",
            "--exec",
            "terrayml",
            "plan",
            "--lock=false",
            "-e",
            ".py",
        ],
        cwd=os.getcwd(),
    )

    try:
        subprocess.run(
            [
                "sam",
                "local",
                "start-api",
                "--hook-name",
                "terraform",
                "--profile",
                aws_profile,
                "--region",
                aws_region,
            ],
            cwd=terrayml_path,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.echo(f"SAM Cli failed: {e}")
    finally:
        nodemon_process.terminate()
        click.echo(f"Nodemon Terminated!")


@click.command()
def init():
    """Change directory to .terraform and run terraform init."""
    terrayml_path = os.path.join(os.getcwd(), ".terraform")

    if not os.path.isdir(terrayml_path):
        click.echo("Error: .terraform directory does not exist!")
        return

    click.echo(f"Changing directory to {terrayml_path} and running terraform init...")

    try:
        subprocess.run(["terraform", "init"], cwd=terrayml_path, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Terraform init failed: {e}")


@click.command()
@click.option(
    "--lock",
    default="true",
    help="Acquire state lock or not.",
)
def plan(lock):
    """Change directory to .terraform and run terraform plan."""
    terrayml_path = os.path.join(os.getcwd(), ".terraform")

    if not os.path.isdir(terrayml_path):
        click.echo("Error: .terraform directory does not exist!")
        return

    click.echo(f"Changing directory to {terrayml_path} and running terraform plan...")

    try:
        if lock == "true":
            subprocess.run(["terraform", "plan"], cwd=terrayml_path, check=True)
        elif lock == "false":
            subprocess.run(
                ["terraform", "plan", "-lock=false"], cwd=terrayml_path, check=True
            )
    except subprocess.CalledProcessError as e:
        click.echo(f"Terraform plan failed: {e}")


@click.command()
def apply():
    """Change directory to .terraform and run terraform apply."""
    terrayml_path = os.path.join(os.getcwd(), ".terraform")

    if not os.path.isdir(terrayml_path):
        click.echo("Error: .terraform directory does not exist!")
        return

    click.echo(f"Changing directory to {terrayml_path} and running terraform apply...")

    try:
        subprocess.run(
            ["terraform", "apply", "-auto-approve"], cwd=terrayml_path, check=True
        )
    except subprocess.CalledProcessError as e:
        click.echo(f"Terraform apply failed: {e}")


@click.command()
@click.option(
    "--delete_tf_files",
    default="false",
    help="Remove .terraform and .tftemp or not.",
)
def destroy(delete_tf_files):
    """Change directory to .terraform and run terraform destroy."""
    terrayml_path = os.path.join(os.getcwd(), ".terraform")

    if not os.path.isdir(terrayml_path):
        click.echo("Error: .terraform directory does not exist!")
        return

    click.echo(
        f"Changing directory to {terrayml_path} and running terraform destroy..."
    )

    try:
        subprocess.run(
            ["terraform", "destroy", "-auto-approve"], cwd=terrayml_path, check=True
        )
        if delete_tf_files == "true":
            for path in [".terraform", ".tftemp"]:
                if os.path.exists(path):
                    shutil.rmtree(path)
                    print(f"🗑️ Terraform folder '{path}' removed successfully.")

    except subprocess.CalledProcessError as e:
        click.echo(f"Terraform destroy failed: {e}")


cli.add_command(generate)
cli.add_command(init)
cli.add_command(plan)
cli.add_command(apply)
cli.add_command(destroy)
cli.add_command(local_api)

if __name__ == "__main__":
    cli()
