import typer
from rich import print
from meshagent.cli import async_typer
from meshagent.cli.helper import get_client, print_json_table, set_active_project, get_active_project

app = async_typer.AsyncTyper()


@app.async_command("list")
async def list():
    client = await get_client()
    projects = await client.list_projects()
    active_project = await get_active_project()
    for project in projects["projects"]:
        if project["id"] == active_project:
            project["name"] = "*" + project["name"]

    print_json_table(projects["projects"], "id", "name")
    await client.close()

@app.async_command("activate")
async def activate(project_id: str):
    client = await get_client()
    try:
        projects = await client.list_projects()
        projects = projects["projects"]
        for project in projects:
            if project["id"] == project_id:
                await set_active_project(project_id=project_id)
                return

        print(f"[red]Invalid project id: {project_id}[/red]")
        raise typer.Exit(code=1)
    finally:
        await client.close()

