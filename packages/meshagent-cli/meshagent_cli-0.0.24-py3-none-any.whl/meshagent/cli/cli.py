import typer

from meshagent.cli import auth
from meshagent.cli import api_keys
from meshagent.cli import projects
from meshagent.cli import sessions
from meshagent.cli import participant_token
from meshagent.cli import agent
from meshagent.cli import messaging
from meshagent.cli import storage
from meshagent.cli import developer
from meshagent.cli import webhook
from meshagent.cli import services
from meshagent.cli import cli_secrets
from meshagent.cli import call
from meshagent.cli import cli_mcp

app = typer.Typer()
app.add_typer(call.app, name="call")
app.add_typer(auth.app, name="auth")
app.add_typer(projects.app, name="project")
app.add_typer(api_keys.app, name="api-key")
app.add_typer(sessions.app, name="session")
app.add_typer(participant_token.app, name="participant-token")
app.add_typer(agent.app, name="agents")
app.add_typer(messaging.app, name="messaging")
app.add_typer(storage.app, name="storage")
app.add_typer(developer.app, name="developer")
app.add_typer(webhook.app, name="webhook")
app.add_typer(services.app, name="service")
app.add_typer(cli_secrets.app, name="secret")
app.add_typer(cli_mcp.app, name="mcp")

if __name__ == "__main__":
    app()
