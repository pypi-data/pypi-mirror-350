# ---------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------
import typer
from rich import print
from typing import Annotated, List, Optional, Dict
from aiohttp import ClientResponseError
from datetime import datetime, timezone
from pydantic_yaml import parse_yaml_raw_as, to_yaml_str
from pydantic import PositiveInt
import pydantic
from typing import Literal
from meshagent.cli import async_typer
from meshagent.cli.helper import get_client, print_json_table, resolve_project_id

# Pydantic basemodels
from meshagent.api.accounts_client import Service, Port

app = async_typer.AsyncTyper()

# ---------------------------------------------------------------------------
#  Utilities
# ---------------------------------------------------------------------------


def _kv_to_dict(pairs: List[str]) -> Dict[str, str]:
    """Convert ["A=1","B=2"] → {"A":"1","B":"2"}."""
    out: Dict[str, str] = {}
    for p in pairs:
        if "=" not in p:
            raise typer.BadParameter(f"'{p}' must be KEY=VALUE")
        k, v = p.split("=", 1)
        out[k] = v
    return out


class PortSpec(pydantic.BaseModel):
    """
    CLI schema for --port.
    Example:
        --port num=8080 type=webserver liveness=/health path=path
    """

    num: PositiveInt
    type: Literal["mcp.sse", "meshagent.callable", "http", "tcp"]
    liveness: str | None = None
    participant_name: str | None = None


def _parse_port_spec(spec: str) -> PortSpec:
    """
    Convert "num=8080 type=webserver liveness=/health" → PortSpec.
    The user should quote the whole string if it contains spaces.
    """
    tokens = spec.strip().split()
    kv: Dict[str, str] = {}
    for t in tokens:
        if "=" not in t:
            raise typer.BadParameter(f"expected key=value, got '{t}'")
        k, v = t.split("=", 1)
        kv[k] = v
    try:
        return PortSpec(**kv)
    except pydantic.ValidationError as exc:
        raise typer.BadParameter(str(exc))


# ---------------------------------------------------------------------------
#  Commands
# ---------------------------------------------------------------------------


@app.async_command("create")
async def service_create(
    *,
    project_id: str = None,
    name: Annotated[str, typer.Option(help="Friendly service name")],
    image: Annotated[str, typer.Option(help="Container image reference")],
    pull_secret: Annotated[
        Optional[str],
        typer.Option("--pull-secret", help="Secret ID for registry"),
    ] = None,
    command: Annotated[
        Optional[str],
        typer.Option("--command", help="Override ENTRYPOINT/CMD"),
    ] = None,
    env: Annotated[List[str], typer.Option("--env", "-e", help="KEY=VALUE")] = [],
    env_secret: Annotated[List[str], typer.Option("--env-secret")] = [],
    runtime_secret: Annotated[List[str], typer.Option("--runtime-secret")] = [],
    room_storage_path: Annotated[
        Optional[str],
        typer.Option("--mount", help="Path inside container to mount room storage"),
    ] = None,
    port: Annotated[
        List[str],
        typer.Option(
            "--port",
            "-p",
            help=(
                "Repeatable. Example:\n"
                '  -p "num=8080 type=[mcp.sse | meshagent.callable | http | tcp] liveness=/health"'
            ),
        ),
    ] = [],
):
    """Create a service attached to the project."""
    client = await get_client()
    try:
        project_id = await resolve_project_id(project_id)

        # ✅ validate / coerce port specs
        port_specs: List[PortSpec] = [_parse_port_spec(s) for s in port]

        ports_dict = {
            ps.num: Port(
                type=ps.type,
                liveness=ps.liveness,
                participant_name=ps.participant_name,
            )
            for ps in port_specs
        } or None

        service_obj = Service(
            id="",
            created_at=datetime.now(timezone.utc).isoformat(),
            name=name,
            image=image,
            command=command,
            pull_secret=pull_secret,
            room_storage_path=room_storage_path,
            environment=_kv_to_dict(env),
            environment_secrets=env_secret or None,
            runtime_secrets=_kv_to_dict(runtime_secret),
            ports=ports_dict,
        )

        try:
            new_id = (
                await client.create_service(project_id=project_id, service=service_obj)
            )["id"]
        except ClientResponseError as exc:
            if exc.status == 409:
                print(f"[red]Service name already in use: {name}[/red]")
                raise typer.Exit(code=1)
            raise
        else:
            print(f"[green]Created service:[/] {new_id}")

    finally:
        await client.close()


@app.async_command("show")
async def service_show(
    *,
    project_id: str = None,
    service_id: Annotated[str, typer.Argument(help="ID of the service to delete")],
):
    """Show a services for the project."""
    client = await get_client()
    try:
        project_id = await resolve_project_id(project_id)
        service = await client.get_service(
            project_id=project_id, service_id=service_id
        )  # → List[Service]
        print(service.model_dump(mode="json"))
    finally:
        await client.close()


@app.async_command("list")
async def service_list(*, project_id: str = None):
    """List all services for the project."""
    client = await get_client()
    try:
        project_id = await resolve_project_id(project_id)
        services: list[Service] = await client.list_services(
            project_id=project_id
        )  # → List[Service]
        print_json_table(
            [svc.model_dump(mode="json") for svc in services],
            "id",
            "name",
            "image",
            "command",
            "room_storage_path",
            "pull_secret",
            "environment_secrets",
            "ports",
        )
    finally:
        await client.close()


@app.async_command("delete")
async def service_delete(
    *,
    project_id: Optional[str] = None,
    service_id: Annotated[str, typer.Argument(help="ID of the service to delete")],
):
    """Delete a service."""
    client = await get_client()
    try:
        project_id = await resolve_project_id(project_id)
        await client.delete_service(project_id=project_id, service_id=service_id)
        print(f"[green]Service {service_id} deleted.[/]")
    finally:
        await client.close()
