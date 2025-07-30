#!/usr/bin/env python3
import click
import asyncio
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
from .engine import CamelRouterEngine


@click.group()
def cli():
    """Camel Router - Multi-language processing engine"""
    pass


@cli.command()
@click.option('--config', '-c', required=True, help='Path to YAML configuration file')
@click.option('--env-file', '-e', default='.env', help='Path to .env file')
@click.option('--route', '-r', help='Run specific route only')
@click.option('--dry-run', is_flag=True, help='Show what would be executed without running')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def run(config, env_file, route, dry_run, verbose):
    """Run routes from configuration file"""

    # Load environment variables
    if os.path.exists(env_file):
        load_dotenv(env_file)
        if verbose:
            click.echo(f"✓ Loaded environment from {env_file}")

    # Load and validate config
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
    except Exception as e:
        click.echo(f"❌ Error loading config: {e}", err=True)
        return

    if verbose:
        click.echo(f"✓ Loaded configuration from {config}")

    # Create engine
    engine = CamelRouterEngine(config_data, verbose=verbose)

    if dry_run:
        engine.dry_run(route)
        return

    # Run routes
    try:
        if route:
            asyncio.run(engine.run_route(route))
        else:
            asyncio.run(engine.run_all_routes())
    except KeyboardInterrupt:
        click.echo("\n🛑 Shutting down...")
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)


@cli.command()
@click.option('--template', '-t', type=click.Choice(['camera', 'grpc', 'email', 'full']),
              default='camera', help='Template type to generate')
@click.option('--output', '-o', default='routes.yaml', help='Output file name')
def init(template, output):
    """Generate sample configuration file"""

    templates = {
        'camera': get_camera_template(),
        'grpc': get_grpc_template(),
        'email': get_email_template(),
        'full': get_full_template()
    }

    template_content = templates[template]

    with open(output, 'w') as f:
        f.write(template_content)

    click.echo(f"✓ Generated {template} template in {output}")
    click.echo(f"📝 Edit the configuration and run: dialogchain run -c {output}")


@cli.command()
@click.option('--config', '-c', required=True, help='Path to YAML configuration file')
def validate(config):
    """Validate configuration file"""
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)

        engine = CamelRouterEngine(config_data)
        errors = engine.validate_config()

        if not errors:
            click.echo("✅ Configuration is valid")
        else:
            click.echo("❌ Configuration errors:")
            for error in errors:
                click.echo(f"  • {error}")

    except Exception as e:
        click.echo(f"❌ Error validating config: {e}", err=True)


def get_camera_template():
    return """# Camera Processing Routes
routes:
  - name: "front_door_camera"
    from: "rtsp://{{CAMERA_USER}}:{{CAMERA_PASS}}@{{CAMERA_IP}}/stream1"
    processors:
      - type: "external"
        command: "python -m ultralytics_processor"
        input_format: "frame_stream"
        output_format: "json"
        config:
          confidence_threshold: 0.6
          target_objects: ["person", "car"]

      - type: "filter"
        condition: "{{confidence}} > 0.7"

      - type: "transform"
        template: "Person detected at {{position}} ({{confidence}}%)"

    to: "email://{{SMTP_SERVER}}:{{SMTP_PORT}}?user={{SMTP_USER}}&password={{SMTP_PASS}}&to={{ALERT_EMAIL}}"

env_vars:
  - CAMERA_USER
  - CAMERA_PASS  
  - CAMERA_IP
  - SMTP_SERVER
  - SMTP_PORT
  - SMTP_USER
  - SMTP_PASS
  - ALERT_EMAIL
"""


def get_grpc_template():
    return """# gRPC Processing Routes
routes:
  - name: "grpc_processor"
    from: "grpc://localhost:50051/ProcessingService/ProcessFrame"
    processors:
      - type: "external"
        command: "go run ./processors/image_processor.go"
        input_format: "protobuf"
        output_format: "json"

    to: "http://localhost:8080/webhook"

  - name: "grpc_server"
    from: "timer://1s"
    processors:
      - type: "external"
        command: "go run ./grpc_server.go"
        async: true
"""


def get_email_template():
    return """# Email Processing Routes  
routes:
  - name: "email_alerts"
    from: "timer://5m"
    processors:
      - type: "aggregate"
        strategy: "collect"
        timeout: "5m"

      - type: "transform"
        template: |
          Alert Summary: {{count}} events
          {{#events}}
          - {{timestamp}}: {{message}}
          {{/events}}

    to: "email://{{SMTP_SERVER}}?user={{SMTP_USER}}&password={{SMTP_PASS}}&to={{RECIPIENTS}}"
"""


def get_full_template():
    return """# Full Configuration Example
routes:
  - name: "camera_processing"
    from: "rtsp://{{CAMERA_USER}}:{{CAMERA_PASS}}@{{CAMERA_IP}}/stream1"
    processors:
      # Object detection using external Python script
      - type: "external"
        command: "python detect_objects.py"
        input_format: "frame_stream"
        output_format: "json"
        config:
          confidence_threshold: 0.6
          model: "yolov8n.pt"

      # Filter high-confidence detections
      - type: "filter" 
        condition: "{{confidence}} > 0.7"

      # Send to gRPC service for additional processing
      - type: "external"
        command: "go run grpc_client.go"
        input_format: "json"
        output_format: "json"
        async: false

      # Transform message
      - type: "transform"
        template: "{{object_type}} detected at {{position}} ({{confidence}}%)"

    # Multiple destinations
    to: 
      - "email://smtp.gmail.com:587?user={{SMTP_USER}}&password={{SMTP_PASS}}&to={{ALERT_EMAIL}}"
      - "http://localhost:8080/webhook"
      - "mqtt://{{MQTT_BROKER}}:1883/alerts/camera"

  - name: "scheduled_health_check"
    from: "timer://10m"
    processors:
      - type: "external"
        command: "curl -f http://localhost:8080/health"
        input_format: "none"
        output_format: "json"

    to: "log://health.log"

env_vars:
  - CAMERA_USER
  - CAMERA_PASS
  - CAMERA_IP
  - SMTP_USER
  - SMTP_PASS
  - ALERT_EMAIL
  - MQTT_BROKER
"""


def main():
    cli()


if __name__ == '__main__':
    main()