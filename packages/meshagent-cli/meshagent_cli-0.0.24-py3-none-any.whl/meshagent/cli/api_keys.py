import typer
from rich import print
from meshagent.cli import async_typer
from meshagent.cli.helper import get_client, print_json_table
from meshagent.cli.helper import set_active_project, get_active_project, resolve_project_id, set_active_api_key, resolve_api_key

app = async_typer.AsyncTyper()


@app.async_command("list")
async def list(*, project_id: str = None):

    project_id = await resolve_project_id(project_id=project_id)

    client = await get_client()
    keys = (await client.list_project_api_keys(project_id=project_id))["keys"]
    if len(keys) > 0:
        print_json_table(keys, "id", "name", "description")
    else:
        print("There are not currently any API keys in the project")
    await client.close()

@app.async_command("create")
async def create(*, project_id: str = None, name: str, description: str = ""):

    project_id = await resolve_project_id(project_id=project_id)

    client = await get_client()
    api_key = await client.create_project_api_key(project_id=project_id, name=name, description=description)
    print(api_key["token"])
    await client.close()


@app.async_command("delete")
async def delete(*, project_id: str = None, id: str):

    project_id = await resolve_project_id(project_id=project_id)

    client = await get_client()
    await client.delete_project_api_key(project_id=project_id, id=id)
    await client.close()


@app.async_command("show")
async def show(*, project_id: str = None, api_key_id: str):
    client = await get_client()
    try:
        project_id = await resolve_project_id(project_id=project_id)

        key = await client.decrypt_project_api_key(project_id=project_id, id=api_key_id)

        print(key["token"])
    
    finally:
        await client.close()


@app.async_command("activate")
async def activate(api_key_id: str, project_id: str = None,):
    client = await get_client()
    try:
        project_id = await resolve_project_id(project_id)
        response = await client.list_project_api_keys(project_id=project_id)
        api_keys = response["keys"]
        for api_key in api_keys:
            if api_key["id"] == api_key_id:
                await set_active_api_key(project_id=project_id, api_key_id=api_key_id)
                return

        print(f"[red]Invalid api key id or project id: {project_id}[/red]")
        raise typer.Exit(code=1)
    finally:
        await client.close()
