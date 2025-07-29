import configparser
from collections import namedtuple
from pathlib import Path
from typing import Optional

import alteia
import typer
from appdirs import user_data_dir

from alteia_cli import __version__, utils

Credentials = namedtuple(
    "Credentials",
    [
        "clientid",
        "clientsecret",
        "username",
        "password",
        "url",
        "proxy_url",
        "insecure",
    ],
)

APPNAME = "alteia"
APPAUTHOR = "Alteia"
DEFAULT_CONF_DIR = Path(user_data_dir(APPNAME, APPAUTHOR))
DEFAULT_CREDENTIAL_PATH = DEFAULT_CONF_DIR / "credentials"
DEFAULT_PROFILE = "default"
DEFAULT_URL = "https://app.alteia.com"
PROFILE_ENV_NAME = "ALTEIA_CLI_PROFILE"

# state is updated in all commands depending on global options
current_state = {
    "profile": DEFAULT_PROFILE,
    "verbose": False,
}


def get_credentials(*, credential_path: Path, profile: str) -> Optional[Credentials]:
    if credential_path.exists():
        try:
            config = configparser.RawConfigParser()
            config.read(credential_path)
            try:
                credentials = Credentials(
                    username=None,
                    password=None,
                    clientid=config[profile]["clientid"],
                    clientsecret=config[profile]["clientsecret"],
                    url=config[profile]["url"],
                    proxy_url=config[profile].get("proxy_url"),
                    insecure=config[profile].get("insecure"),
                )
            except (configparser.MissingSectionHeaderError, KeyError):
                credentials = Credentials(
                    clientid=None,
                    clientsecret=None,
                    username=config[profile]["username"],
                    password=config[profile]["password"],
                    url=config[profile]["url"],
                    proxy_url=config[profile].get("proxy_url"),
                    insecure=config[profile].get("insecure"),
                )

            return credentials

        except (configparser.MissingSectionHeaderError, KeyError):
            return None
    else:
        return None


def check_credentials(credentials: Credentials) -> bool:
    try:
        connection = {"max_retries": 1}
        if credentials.insecure:
            connection["disable_ssl_certificate"] = True
        alteia.SDK(
            user=credentials.username,
            password=credentials.password,
            url=credentials.url,
            proxy_url=credentials.proxy_url,
            connection=connection,
            service=f"alteia-cli/{__version__}",
        )
    except Exception:
        return False

    return True  # Connection OK = valid credentials


def save_config(credentials: Credentials, *, credential_path: Path, profile: str) -> None:
    config = configparser.RawConfigParser()
    if credential_path.exists():
        # load existing config file, only the specified section will be replaced
        config.read(credential_path)
    credential_dict = credentials._asdict()

    if credentials.proxy_url is None:
        credential_dict.pop("proxy_url")
    if credentials.clientid is None:
        credential_dict.pop("clientid")
    if credentials.clientsecret is None:
        credential_dict.pop("clientsecret")

    config[profile] = credential_dict

    if not credential_path.parent.exists():
        Path(credential_path.parent).mkdir(parents=True, exist_ok=True)

    with open(credential_path, "w") as configfile:
        config.write(configfile)


def setup(
    credential_path: Path = DEFAULT_CREDENTIAL_PATH,
    *,
    profile: Optional[str] = None,
    insecure=False,
) -> Credentials:
    if profile is None:
        profile = str(current_state["profile"])

    welcome_msg = typer.style(
        "Alright. Let's configure your credentials to connect to the platform " f"(profile={profile}).",
        fg=typer.colors.GREEN,
        bold=True,
    )
    typer.secho(welcome_msg)
    print()

    if insecure:
        confirmation_msg = typer.style(
            "Profile will be configured in insecured mode. Meaning that SSL certificate "
            "will not be verified. Do you confirm this operation ?",
            fg=typer.colors.YELLOW,
            bold=True,
        )

        typer.confirm(confirmation_msg, abort=True)

    existing_credentials = get_credentials(credential_path=credential_path, profile=profile)

    if existing_credentials:
        confirmation_msg = typer.style(
            f"Profile '{profile}' already exists in the configuration file "
            f"({credential_path}). Do you want to replace it ?",
            fg=typer.colors.RED,
        )
        typer.confirm(confirmation_msg, abort=True)
        username = typer.prompt(
            typer.style("Email", bold=True),
            type=str,
            default=existing_credentials.username,
        )
        password = typer.prompt(
            typer.style("Password ", bold=True) + "[Press ENTER to keep password unchanged]",
            type=str,
            default=existing_credentials.password,
            show_default=False,
            hide_input=True,
        )
        url = typer.prompt(
            typer.style("Platform URL", bold=True),
            type=str,
            default=existing_credentials.url,
        )
        proxy_url = typer.prompt(
            typer.style("Proxy URL", bold=True),
            type=str,
            default=existing_credentials.proxy_url or "",
        )

    else:
        username = typer.prompt(typer.style("Email", bold=True), type=str)
        password = typer.prompt(
            typer.style("Password", bold=True) + " (will not be displayed)",
            type=str,
            hide_input=True,
        )
        url = typer.prompt(
            typer.style("Platform URL", bold=True) + " (or press ENTER to set {})".format(DEFAULT_URL),
            type=str,
            default=DEFAULT_URL,
            show_default=False,
        )
        proxy_url = typer.prompt(
            typer.style("Proxy URL", bold=True) + " (or press ENTER if not applicable)",
            type=str,
            default="",
            show_default=False,
        )

    if proxy_url == "":
        proxy_url = None

    credentials = Credentials(
        clientid=None,
        clientsecret=None,
        username=username,
        password=password,
        url=url,
        proxy_url=proxy_url,
        insecure=insecure if insecure else None,
    )
    print()

    print("Checking credentials...")
    with utils.spinner():
        valid = check_credentials(credentials)

    if not valid:
        invalid_cred_msg = typer.style(
            "✖ Cannot connect with the supplied credentials. " "Do you want to save this configuration anyway ?",
            fg=typer.colors.RED,
        )
        typer.confirm(invalid_cred_msg, abort=True)
    else:
        valid_cred_msg = typer.style("✓ Connection OK with these credentials", fg=typer.colors.GREEN)
        typer.secho(valid_cred_msg)

    save_config(credentials, credential_path=credential_path, profile=profile)

    saved_cred_msg = typer.style("✓ Credentials saved in {!r}".format(credential_path), fg=typer.colors.GREEN)
    typer.secho(saved_cred_msg)
    print()

    return credentials
