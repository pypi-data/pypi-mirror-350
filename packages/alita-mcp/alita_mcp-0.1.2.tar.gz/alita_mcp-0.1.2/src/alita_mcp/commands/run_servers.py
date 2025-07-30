import asyncio
import sys
from uuid import uuid4

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from ..config import load_config
from ..utils.menu import show_menu
from ..utils.sio import start_socket_connection


def run_servers():
    config = load_config()
    connection_uid = str(uuid4())

    all_tools = asyncio.run(_get_all_tools(config["servers"]))
    tree = {}
    for server in all_tools:
        tools = [tool["name"] for tool in server.get("tools", [])]
        tree[server["name"]] = tools

    try:
        selection = show_menu(tree)

        filtered_servers = selection.keys()
        filtered_tools = []
        for server in all_tools:
            if server["name"] in filtered_servers:
                selected_server = server.copy()
                selected_server["tools"] = [
                    tool for tool in server.get("tools", [])
                    if tool["name"] in selection[server["name"]]
                ]
                filtered_tools.append(selected_server)

        sio = start_socket_connection(config, connection_uid, filtered_tools)

        while True:
            user_input = input("").strip()
            if user_input.lower() == "1":
                print("Emitting event...")
    except KeyboardInterrupt:
        print("\nExiting application...")
        sio.disconnect()
        sys.exit(0)


async def _process_server(server_name, server_conf):
    if "type" in server_conf:
        if server_conf["type"].lower() == "stdio":
            print(f"CLIENT FOR STDIO SERVER: {server_name}")
            server_parameters = StdioServerParameters(
                **server_conf
            )
            async with stdio_client(server_parameters) as (read, write):
                async with ClientSession(
                        read, write
                ) as session:
                    await session.initialize()
                    tools_response = await session.list_tools()
                    return {"name": server_name, "tools": [dict(tool) for tool in tools_response.tools]}

        elif server_conf["type"].lower() == "sse":
            print(f"CLIENT FOR SSE SERVER: {server_conf['url']}")
            async with sse_client(server_conf["url"], server_conf["headers"]) as streams:
                async with ClientSession(*streams) as session:
                    await session.initialize()
                    tools_response = await session.list_tools()
                    return {"name": server_name, "tools": [dict(tool) for tool in tools_response.tools]}


async def _get_all_tools(servers=[]):
    tasks = [
        _process_server(server_name, server_conf)
        for server_name, server_conf in servers.items()
    ]
    results = await asyncio.gather(*tasks)
    return results
