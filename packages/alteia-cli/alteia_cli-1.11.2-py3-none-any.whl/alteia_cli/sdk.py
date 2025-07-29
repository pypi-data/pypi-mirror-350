from pathlib import Path
from typing import Optional

import alteia

from alteia_cli import __version__, config


def alteia_sdk(
    credential_path: Path = config.DEFAULT_CREDENTIAL_PATH,
    *,
    profile: Optional[str] = None,
) -> alteia.SDK:
    if profile is None:
        profile = str(config.current_state["profile"])

    credentials = config.get_credentials(credential_path=credential_path, profile=profile)
    if not credentials:
        credentials = config.setup(credential_path=credential_path, profile=profile)

    if config.current_state["verbose"]:
        print("Alteia Platform URL: ", credentials.url)
        print("Alteia Platform User:", credentials.username or credentials.clientid)
        print()

    connection = None
    if credentials.insecure:
        connection = {"disable_ssl_certificate": True}

    if credentials.username and credentials.password:
        alteia_sdk = alteia.SDK(
            user=credentials.username,
            password=credentials.password,
            url=credentials.url,
            proxy_url=credentials.proxy_url,
            service=f"alteia-cli/{__version__}",
            connection=connection,
        )
    else:
        alteia_sdk = alteia.SDK(
            client_id=credentials.clientid,
            client_secret=credentials.clientsecret,
            url=credentials.url,
            proxy_url=credentials.proxy_url,
            service=f"alteia-cli/{__version__}",
            connection=connection,
        )

    return alteia_sdk
