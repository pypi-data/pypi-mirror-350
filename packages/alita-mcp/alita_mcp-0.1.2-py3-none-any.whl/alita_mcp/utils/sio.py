import asyncio
import threading

import socketio
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client


def start_socket_connection(config, connection_uid, all_tools):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to platform")

    @sio.event
    def disconnect():
        print("Disconnected from Socket.IO server")

    @sio.event
    def on_connect(data):
        if "server" in data:
            print(f"Received REQUEST: {data}")
            print(f"Received SERVER CONF : {config["servers"][data["server"]]}")

            tool_result = asyncio.run(_mcp_tolls_call(config["servers"][data["server"]], data["params"]))

            print(f"SEND TO THE ELITEA PLATFORM TOOL RESULT : {tool_result}")
            sio.emit("mcp_tool_call", {"data": tool_result, "tool_call_id": data["tool_call_id"]})
            print(f"READY SEND")

    sio.connect(config["deployment_url"], headers={
        'Authorization': f"Bearer {config['auth_token']}"})

    sio.on('mcp_connect', on_connect)

    def socketio_background_task():
        sio.wait()

    socketio_thread = threading.Thread(target=socketio_background_task, daemon=True)
    socketio_thread.start()

    sio.emit("mcp_connect", {
        "connection_uid": connection_uid,
        "project_id": config["project_id"],
        "toolkit_configs": all_tools
    })

    return sio


async def _mcp_tolls_call(server_conf, params):
    if "type" in server_conf:
        if server_conf["type"].lower() == "stdio":
            pass
            server_parameters = StdioServerParameters(
                **server_conf
            )
            async with stdio_client(server_parameters) as (read, write):
                async with ClientSession(
                        read, write
                ) as session:
                    await session.initialize()
                    tool_result = await session.call_tool(params["name"], params["arguments"])

                    print(f"TOOL RESULT:\n {tool_result}")
                    return tool_result.content[0].text

        elif server_conf["type"].lower() == "sse":
            print(f"CLIENT FOR SSE SERVER: {server_conf['url']}")
            async with sse_client(server_conf["url"], server_conf["headers"]) as streams:
                async with ClientSession(*streams) as session:
                    await session.initialize()
                    tool_result = await session.call_tool(params["name"], params["arguments"])

                    print(f"TOOL RESULT:\n {tool_result}")
                    return tool_result.content[0].text