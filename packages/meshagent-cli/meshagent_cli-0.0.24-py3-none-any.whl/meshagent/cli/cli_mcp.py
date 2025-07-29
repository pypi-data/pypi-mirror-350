
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters

import typer
from rich import print
from typing import Annotated, Optional

from meshagent.api.helpers import meshagent_base_url, websocket_room_url
from meshagent.api import RoomClient, ParticipantToken, WebSocketClientProtocol, RoomException
from meshagent.cli import async_typer
from meshagent.cli.helper import get_client, print_json_table, set_active_project, resolve_project_id
from meshagent.cli.helper import set_active_project, get_active_project, resolve_project_id, resolve_api_key, resolve_token_jwt

from meshagent.tools.hosting import RemoteToolkit, RemoteToolkitServer

from meshagent.mcp import MCPToolkit
from pathlib import Path

from meshagent.api.services import ServiceHost
import os


import shlex

app = async_typer.AsyncTyper()

@app.async_command("sse")
async def sse(*, project_id: str = None, room: Annotated[str, typer.Option()], token_path: Annotated[Optional[str], typer.Option()] = None, api_key_id: Annotated[Optional[str], typer.Option()] = None, name: Annotated[str, typer.Option(..., help="Participant name")] = "cli", role: str = "tool", url: Annotated[str, typer.Option()]):
    account_client = await get_client()
    try:
        project_id = await resolve_project_id(project_id=project_id)
        api_key_id = await resolve_api_key(project_id, api_key_id)

        jwt = await resolve_token_jwt(project_id=project_id, api_key_id=api_key_id, token_path=token_path, name=name, role=role, room=room)
       
        print("[bold green]Connecting to room...[/bold green]")
        async with RoomClient(protocol=WebSocketClientProtocol(url=websocket_room_url(room_name=room, base_url=meshagent_base_url()), token=jwt)) as client:
            
            async with sse_client(url) as (read_stream, write_stream):

                async with ClientSession(read_stream=read_stream, write_stream=write_stream) as session:
                    
                    mcp_tools_response = await session.list_tools()
                    
                    toolkit = MCPToolkit(name=name, session=session, tools=mcp_tools_response.tools)
                    
                    remote_toolkit = RemoteToolkit(name=toolkit.name, tools=toolkit.tools, title=toolkit.title, description=toolkit.description)

                    await remote_toolkit.start(room=client)
                    try:
                        await client.protocol.wait_for_close()
                    except KeyboardInterrupt:
                        await remote_toolkit.stop()


    except RoomException as e:
        print(f"[red]{e}[/red]")
    finally:
        await account_client.close()



@app.async_command("stdio")
async def stdio(*, project_id: str = None, room: Annotated[str, typer.Option()], token_path: Annotated[Optional[str], typer.Option()] = None, api_key_id: Annotated[Optional[str], typer.Option()] = None, name: Annotated[str, typer.Option(..., help="Participant name")] = "cli", role: str = "tool", command: Annotated[str, typer.Option()]):
    account_client = await get_client()
    try:
        project_id = await resolve_project_id(project_id=project_id)
        api_key_id = await resolve_api_key(project_id, api_key_id)

        jwt = await resolve_token_jwt(project_id=project_id, api_key_id=api_key_id, token_path=token_path, name=name, role=role, room=room)

        print("[bold green]Connecting to room...[/bold green]")
        async with RoomClient(protocol=WebSocketClientProtocol(url=websocket_room_url(room_name=room, base_url=meshagent_base_url()), token=jwt)) as client:
            
            parsed_command = shlex.split(command)

            async with stdio_client(StdioServerParameters(
                    command=parsed_command[0],  # Executable
                    args=parsed_command[1:],  # Optional command line arguments
                    env=None,  # Optional environment variables
                )) as (read_stream, write_stream):

                async with ClientSession(read_stream=read_stream, write_stream=write_stream) as session:
                    
                    mcp_tools_response = await session.list_tools()
                    
                    toolkit = MCPToolkit(name=name, session=session, tools=mcp_tools_response.tools)
                    
                    remote_toolkit = RemoteToolkit(name=toolkit.name, tools=toolkit.tools, title=toolkit.title, description=toolkit.description)

                    await remote_toolkit.start(room=client)
                    try:
                        await client.protocol.wait_for_close()
                    except KeyboardInterrupt:
                        await remote_toolkit.stop()


    except RoomException as e:
        print(f"[red]{e}[/red]")
    finally:
        await account_client.close()


@app.async_command("stdio-service")
async def stdio_host(*,  command: Annotated[str, typer.Option()],  host: Annotated[Optional[str], typer.Option()] = None, port: Annotated[Optional[int], typer.Option()] = None, webhook_secret: Annotated[Optional[str], typer.Option()] = None, path: Annotated[Optional[str], typer.Option()] = None):
    
    try:
        
        parsed_command = shlex.split(command)
      
        async with stdio_client(StdioServerParameters(
                command=parsed_command[0],  # Executable
                args=parsed_command[1:],  # Optional command line arguments
                env=None,  # Optional environment variables
            )) as (read_stream, write_stream):

            async with ClientSession(read_stream=read_stream, write_stream=write_stream) as session:
                
                mcp_tools_response = await session.list_tools()
                
                toolkit = MCPToolkit(name="mcp", session=session, tools=mcp_tools_response.tools)
                
                if port == None:

                    port = int(os.getenv("MESHAGENT_PORT", "8080"))

                if host == None:

                    host = "localhost"

                service_host = ServiceHost(
                    host=host,
                    port=port,
                    webhook_secret=webhook_secret
                )

                if path == None:
                    path = "/service"

                print(f"[bold green]Starting service host on {host}:{port}{path}...[/bold green]")
                @service_host.path(path=path)
                class CustomToolkit(RemoteToolkit):
                    def __init__(self):
                        super().__init__(name=toolkit.name, tools=toolkit.tools, title=toolkit.title, description=toolkit.description)

                
                await service_host.run()


    except RoomException as e:
        print(f"[red]{e}[/red]")

