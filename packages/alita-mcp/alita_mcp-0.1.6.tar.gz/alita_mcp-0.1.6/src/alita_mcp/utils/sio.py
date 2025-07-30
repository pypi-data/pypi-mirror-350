import asyncio
import threading

import socketio
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from .session_manager import get_session_manager


def start_socket_connection(config, connection_uid, all_tools):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to platform")

    @sio.event
    def disconnect():
        print("Disconnected from Socket.IO server")
        # Clean up persistent sessions when disconnecting
        session_manager = get_session_manager()
        try:
            session_manager.cleanup_all()
            print("Cleaned up persistent sessions")
        except Exception as e:
            print(f"Error during session cleanup: {e}")

    @sio.event
    def on_connect(data):
        if "server" in data:
            print(f"Received REQUEST: {data}")
            print(f"Received SERVER CONF : {config["servers"][data["server"]]}")

            # Use synchronous wrapper to avoid asyncio.run() conflicts
            tool_result = _mcp_tools_call_sync(
                config["servers"][data["server"]], 
                data["params"], 
                server_name=data["server"]
            )

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


def _mcp_tools_call_sync(server_conf, params, server_name=None):
    """Synchronous wrapper for MCP tool calls that handles both stateful and stateless sessions."""
    session_manager = get_session_manager()
    
    # Check if this server should use stateful sessions
    if session_manager.is_stateful(server_conf) and server_name:
        # Use persistent session with recovery
        try:
            result = session_manager.call_tool_with_recovery_sync(server_name, server_conf, params)
            print(f"TOOL RESULT (stateful session):\n {result}")
            return result
        except Exception as e:
            print(f"Failed to call tool with stateful session: {e}")
            print("Falling back to stateless session...")
            # Fall through to stateless mode as fallback
    
    # Use stateless session (original behavior) via async wrapper
    async def _stateless_call():
        return await _mcp_tolls_call(server_conf, params, server_name)
    
    # Run in session manager's event loop to avoid conflicts
    return session_manager._run_in_loop(_stateless_call())


async def _mcp_tolls_call(server_conf, params, server_name=None):
    """Async function for stateless MCP tool calls."""
    # Use stateless session (original behavior)
    if "type" in server_conf:
        if server_conf["type"].lower() == "stdio":
            server_parameters = StdioServerParameters(
                **server_conf
            )
            async with stdio_client(server_parameters) as (read, write):
                async with ClientSession(
                        read, write
                ) as session:
                    await session.initialize()
                    tool_result = await session.call_tool(params["name"], params["arguments"])

                    print(f"TOOL RESULT (stateless session):\n {tool_result}")
                    return tool_result.content[0].text

        elif server_conf["type"].lower() == "sse":
            async with sse_client(server_conf["url"], server_conf.get("headers", {})) as streams:
                async with ClientSession(*streams) as session:
                    await session.initialize()
                    tool_result = await session.call_tool(params["name"], params["arguments"])

                    print(f"TOOL RESULT (stateless session):\n {tool_result}")
                    return tool_result.content[0].text