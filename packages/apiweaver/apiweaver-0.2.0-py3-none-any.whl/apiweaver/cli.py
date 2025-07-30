"""
Command-line interface for APIWeaver.
"""

import json
import click
from pathlib import Path
from typing import Optional
from .server import APIWeaver


@click.group()
def main():
    """APIWeaver - Convert any web API into an MCP server."""
    pass


@main.command()
@click.option("--name", default="APIWeaver", help="Server name")
@click.option("--config", type=click.Path(exists=True), help="API configuration file (JSON)")
@click.option("--transport", default="stdio", type=click.Choice(["stdio", "sse", "streamable-http"]), help="Transport type")
@click.option("--host", default="127.0.0.1", help="Host for HTTP transports")
@click.option("--port", default=8000, type=int, help="Port for HTTP transports")
@click.option("--path", default="/mcp", help="Path for HTTP transports")
def run(name: str, config: Optional[str], transport: str, host: str, port: int, path: str):
    """Run the APIWeaver server."""
    
    # Create server
    server = APIWeaver(name=name)
    
    # Load configuration if provided
    if config:
        config_path = Path(config)
        if config_path.exists():
            with open(config_path, 'r') as f:
                api_config = json.load(f)
            
            # Register API from config file
            # This would need to be done through the MCP protocol
            # For now, we'll just start the server
            click.echo(f"Loaded configuration from {config}")
    
    # Run server with appropriate transport
    if transport == "stdio":
        click.echo(f"Starting {name} server on STDIO transport...")
        server.run()
    elif transport == "streamable-http":
        click.echo(f"Starting {name} server on Streamable HTTP transport at http://{host}:{port}{path}")
        server.run(transport="streamable-http", host=host, port=port, path=path)
    else:  # sse
        click.echo(f"Starting {name} server on SSE transport at http://{host}:{port}{path}")
        server.run(transport="sse", host=host, port=port, path=path)


if __name__ == "__main__":
    main()
