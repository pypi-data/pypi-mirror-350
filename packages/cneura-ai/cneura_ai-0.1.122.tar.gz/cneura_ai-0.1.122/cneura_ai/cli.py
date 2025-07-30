import os
import json
import click
from jinja2 import Template
from cneura_ai.commands import DockerManager
from cneura_ai.config import CLIConfig

docker_manager = DockerManager()

@click.group()
@click.version_option(CLIConfig.VERSION, message="🚀 CNeura AI version %(version)s")
@click.option("--config", type=click.Path(exists=True), help="Override default config file (JSON)")
def cli(config):
    """🔧 CNeura CLI - Autonomous Service Orchestration Toolkit"""
    CLIConfig.ensure_paths()
    if config:
        try:
            CLIConfig.apply_override(config)
            click.echo(f"✅ Loaded custom configuration from: {config}")
        except Exception as e:
            click.echo(f"❌ Error loading config override: {e}")

@cli.command()
def version():
    """📦 Show the current version."""
    click.echo(f"🚀 CNeura AI version {CLIConfig.VERSION}")

@cli.command()
def run():
    """🛠️ Launch all microservices."""
    click.echo("🔄 Starting services...")

    config_path = CLIConfig.run_config_override or CLIConfig.DEFAULT_RUN_CONFIG

    # Generate config if it doesn't exist
    if not os.path.exists(config_path):
        try:
            with open(CLIConfig.DEFAULT_RUN_CONFIG_TEMPLATE) as f:
                template = Template(f.read())

            context = {
                k: getattr(CLIConfig, k)
                for k in dir(CLIConfig)
                if not k.startswith("__") and not callable(getattr(CLIConfig, k))
            }
            rendered = template.render(**context)
            data = json.loads(rendered)

            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(data, f, indent=2)

            click.echo(f"✅ Generated run.json at: {config_path}")
        except Exception as e:
            click.echo(f"❌ Failed to generate run.json: {e}")
            return

    # Run services
    try:
        docker_manager.load_from_config(config_path)
        click.echo("✅ Microservices started successfully.")
    except Exception as e:
        click.echo(f"❌ Error starting services: {e}")

@cli.command()
@click.argument("service_name")
def status(service_name):
    """📋 Check the status of a service."""
    click.echo(f"🔍 Checking status for: {service_name}")
    containers = docker_manager.list_running_containers()
    matched = [c for c in containers if service_name in c["name"]]

    if matched:
        for c in matched:
            click.echo(f"✅ {c['name']} | Status: {c['status']} | Ports: {c['ports']}")
    else:
        click.echo(f"⚠️ No running containers match service name '{service_name}'.")

@cli.command()
@click.argument("service_name")
def delete(service_name):
    """🗑️ Stop and delete a specific service."""
    click.confirm(f"⚠️ Are you sure you want to delete service '{service_name}'?", abort=True)
    docker_manager.delete_container(service_name)
    click.echo(f"✅ Deleted service '{service_name}'.")

@cli.command(name="list")
def list_services():
    """📦 List all running services."""
    containers = docker_manager.list_running_containers()

    if not containers:
        click.echo("🚫 No running containers.")
        return

    click.echo("🟢 Active Services:")
    for c in containers:
        click.echo(f" - {c['name']} | Status: {c['status']} | Ports: {c['ports']}")

@cli.command()
def stop_all():
    """🛑 Stop all running containers."""
    click.confirm("⚠️ This will stop ALL running containers. Continue?", abort=True)
    docker_manager.stop_all()
    click.echo("🛑 All containers stopped.")

@cli.command()
def init():
    """⚙️ Start initial required containers from template."""
    try:
        with open(CLIConfig.DEFAULT_INIT_CONFIG_TEMPLATE) as f:
            template = Template(f.read())

        context = {
            k: getattr(CLIConfig, k)
            for k in dir(CLIConfig)
            if not k.startswith("__") and not callable(getattr(CLIConfig, k))
        }

        rendered = template.render(**context)
        path = CLIConfig.init_config_override or CLIConfig.DEFAULT_INIT_CONFIG
        data = json.loads(rendered)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        click.echo(f"✅ Generated init.json at: {path}")
    except Exception as e:
        click.echo(f"❌ Failed to generate init config: {e}")
        return

    try:
        docker_manager.load_from_config(path)
        click.echo("✅ Initial containers started.")
    except Exception as e:
        click.echo(f"❌ Failed to start initial containers: {e}")


@cli.command()
@click.argument("queue_name")
@click.option("--file", "json_file", type=click.Path(exists=True), required=True, help="Path to JSON file to send.")
def send_payload(queue_name, json_file):
    """
    Send a JSON payload (from a file) to a specified RabbitMQ queue.
    """
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        click.echo(f"❌ Failed to read JSON file: {e}")
        return

    try:
        import pika

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=CLIConfig.RABBITMQ_HOST,
            port=CLIConfig.RABBITMQ_PORT,
            virtual_host=CLIConfig.RABBITMQ_VHOST,
            credentials=pika.PlainCredentials(CLIConfig.RABBITMQ_USER, CLIConfig.RABBITMQ_PASS)
        ))

        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        connection.close()
        click.echo(f"✅ Payload from '{json_file}' sent to queue '{queue_name}'.")

    except Exception as e:
        click.echo(f"❌ Failed to send payload to RabbitMQ: {e}")


def main():
    cli()

if __name__ == "__main__":
    main()
