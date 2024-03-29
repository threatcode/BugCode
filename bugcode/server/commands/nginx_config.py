"""
Bugcode Penetration Test IDE
Copyright (C) 2020  Threatcode LLC (https://threatcode.github.io/bugcode/)
See the file 'doc/LICENSE' for the license information
"""
# Standard library imports
import sys
from pathlib import Path

# Related third party imports
import click
from jinja2 import Environment, FileSystemLoader


def generate_nginx_config(fqdn, port, ws_port, ssl_certificate, ssl_key, multitenant_url):
    click.echo(f"Generating Bugcode nginx config for server: {fqdn}")
    click.echo("Bugcode")
    if multitenant_url:
        click.echo(f"- Multitenant URL: /{multitenant_url}/")
    click.echo(f"- Port: {port}")
    click.echo(f"- Websocket Port: {ws_port}")
    click.echo(f"SSL: certificate [{ssl_certificate}] - key [{ssl_key}]")
    confirm = click.prompt('Confirm [Y/n]', type=bool)
    if confirm:
        version = sys.version_info
        static_path = f"/opt/bugcode/lib/python{version.major}.{version.minor}/site-packages/bugcode/server/www"
        templates_path = Path(__file__).parent / 'templates'
        file_loader = FileSystemLoader(templates_path)
        env = Environment(loader=file_loader, autoescape=True)
        template = env.get_template('nginx_config.j2')
        output = template.render(**{'fqdn': fqdn, 'static_path': static_path, 'bugcode_port': port,
                                    'bugcode_ws_port': ws_port, 'ssl_certificate': ssl_certificate, 'ssl_key': ssl_key,
                                    'multitenant_url': multitenant_url})
        click.echo("NGINX Config\n#####################################\n\n")
        click.echo(output)
