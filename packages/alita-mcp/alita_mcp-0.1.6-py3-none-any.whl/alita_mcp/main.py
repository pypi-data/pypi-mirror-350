import argparse
import threading
import time

from alita_mcp.commands.bootstrap_servers import bootstrap_servers
from alita_mcp.commands.run_servers import run_servers

from .config import (set_bootstrap_config, get_bootstrap_config, 
                    interactive_bootstrap)
from .clients.alita import Agent, Agents
from .server.mcp import run


def main(project_id=None, application_id=None, version_id=None, transport="stdio", port=8000):
    # Get configuration from bootstrap
    config = get_bootstrap_config()
    deployment_url = config.get("deployment_url")
    auth_token = config.get("auth_token")
    host = config.get("host", "0.0.0.0")
    port = config.get("port", 8000)
    
    if not deployment_url or not auth_token:
        print("Error: Configuration missing. Please run bootstrap first.")
        return
    
    if not project_id:
        print("Error: Project ID is required")
        return
        
    if not application_id:
        # Using project-level agents when only project_id is provided
        client = Agents(base_url=deployment_url,
                        project_id=project_id,
                        auth_token=auth_token).agents
    else:
        # Using specific agent when application_id is provided
        client = Agent(base_url=deployment_url,
                    project_id=project_id,
                    auth_token=auth_token,
                    app_id = application_id,
                    version_id=version_id)
        
    print(config)
    
    print(f"Starting MCP server for project {project_id}")
    if application_id:
        print(f"Using application: {application_id}" + 
              (f", version: {version_id}" if version_id else ""))
    else:
        print("Using all available project agents")
    run(client, transport=transport, host=host, port=port)

def bootstrap(deployment_url=None, auth_token=None, host='0.0.0.0', port=8000):
    """
    Bootstrap the client with deployment URL and authentication token.
    If parameters are not provided, runs in interactive mode.
    """
    if deployment_url is not None and auth_token is not None:
        # Non-interactive mode with command line arguments
        config = set_bootstrap_config(deployment_url, auth_token, host, port)
    else:
        # Interactive mode
        config = interactive_bootstrap()
    print(f"Deployment URL: {config.get('deployment_url')}")
    
    auth_token = config.get('auth_token')
    if auth_token:
        masked_token = '*' * 8 + auth_token[-4:] if len(auth_token) > 4 else '*' * 8
        print(f"Auth Token: {masked_token}")
    
    if config["deployment_url"]:
        bootstrap_servers(config)

def cli():
    parser = argparse.ArgumentParser(description='MCP Client')
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Main command
    main_parser = subparsers.add_parser("run", help="Run the MCP client")
    main_parser.add_argument('--project_id', type=str, help='Project ID')
    main_parser.add_argument('--app_id', type=str, help='Application ID')
    main_parser.add_argument('--version_id', type=str, help='Version ID')
    main_parser.add_argument('--transport', type=str, choices=['stdio', 'sse'], 
                            default='stdio', help='Transport type (stdio or sse)')
    main_parser.add_argument('--port', type=int, default=8000, 
                            help='Port to listen on (for SSE transport)')
    
    # Bootstrap command - make arguments optional
    bootstrap_parser = subparsers.add_parser("bootstrap", help="Set deployment URL and auth token")
    bootstrap_parser.add_argument('--deployment_url', type=str, help='Deployment URL')
    bootstrap_parser.add_argument('--auth_token', type=str, help='Authentication token')
    bootstrap_parser.add_argument('--host', type=str, default='0.0.0.0', help='Host for SSE transport')
    bootstrap_parser.add_argument('--port', type=int, default=8000, help='Port for SSE transport')

    subparsers.add_parser("serve", help="Connect to platform and makes it possible to run MCP servers on user's environment")
    
    args = parser.parse_args()
    
    if args.command == "bootstrap":
        bootstrap(
            deployment_url=args.deployment_url if hasattr(args, 'deployment_url') else None,
            auth_token=args.auth_token if hasattr(args, 'auth_token') else None,
            host=args.host if hasattr(args, 'host') else '0.0.0.0',
            port=args.port if hasattr(args, 'port') else 8000
        )
    elif args.command == "serve":
        run_servers()
    elif args.command == "run" or args.command is None:
        main(
            project_id=args.project_id if hasattr(args, 'project_id') else None,
            application_id=args.app_id if hasattr(args, 'app_id') else None,
            version_id=args.version_id if hasattr(args, 'version_id') else None,
            transport=args.transport if hasattr(args, 'transport') else "stdio",
            port=args.port if hasattr(args, 'port') else 8000
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()