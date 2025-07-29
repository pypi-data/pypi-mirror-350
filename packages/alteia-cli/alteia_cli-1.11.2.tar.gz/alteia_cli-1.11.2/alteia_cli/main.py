import typer

import alteia_cli.custom_analytics
import alteia_cli.plugins
from alteia_cli import config
from alteia_cli.loader import Loader

app = typer.Typer()
loader = Loader(app)
loader.extend_app(alteia_cli.custom_analytics.__path__)  # type: ignore
loader.extend_app(alteia_cli.plugins.__path__)


@app.command()
def configure(
    profile: str = typer.Argument(
        default=config.DEFAULT_PROFILE,
        help="Alteia CLI Profile to configure",
        envvar=config.PROFILE_ENV_NAME,
    ),
    insecure: bool = typer.Option(
        None,
        "--insecure",
        help="Allow insecure connection for profile, disable SSL certificate verification",
    ),
):
    """
    Configure platform credentials.

    You can configure multiples credential profiles by specifying
    a different profile name for each one.
    """
    config.setup(profile=profile, insecure=insecure)


def display_version(value: bool):
    if value:
        print("Alteia CLI Version:", alteia_cli.__version__)
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    profile: str = typer.Option(
        config.DEFAULT_PROFILE, "--profile", "-p", help="Alteia CLI Profile", envvar=config.PROFILE_ENV_NAME
    ),
    version: bool = typer.Option(None, "--version", help="Display the CLI version and exit", callback=display_version),
    verbose: bool = typer.Option(None, "--verbose", help="Display more info during the run"),
):
    """
    CLI for Alteia Platform.
    """
    if profile:
        config.current_state["profile"] = str(profile)

    if verbose:
        config.current_state["verbose"] = True
        print("Alteia CLI Version:", alteia_cli.__version__)
        print("Alteia CLI Profile:", config.current_state["profile"])
        print("About to execute command:", ctx.invoked_subcommand)
        print()


if __name__ == "__main__":
    app()
