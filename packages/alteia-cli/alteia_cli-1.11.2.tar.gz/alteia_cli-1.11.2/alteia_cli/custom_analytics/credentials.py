import json
from enum import Enum
from pathlib import Path
from typing import Dict, List, Mapping, cast

import typer
from alteia.core.errors import ResponseError
from alteia.core.resources.resource import Resource, ResourcesWithTotal
from PyInquirer import prompt
from tabulate import tabulate

from alteia_cli import AppDesc, utils
from alteia_cli.color_manager import UniqueColor
from alteia_cli.sdk import alteia_sdk

app = typer.Typer()
app_desc = AppDesc(app, name="credentials", help="Interact with Docker registry credentials.")


EXIT = "Exit"


class CredentialsType(str, Enum):
    docker = "docker"
    object_storage = "object-storage"
    stac_catalog = "stac-catalog"


class ObjectStorageType(str, Enum):
    s3 = "s3"
    azure_blob = "azure-blob"
    gcp = "google-cloud-storage"


@app.command(name="create")
def create(
    filepath: Path = typer.Option(
        ...,  # '...' in typer.Option() makes the option required
        exists=True,
        readable=True,
        help="Path of the Credential JSON file.",
    ),
    company: str = typer.Option(default=None, help="Company identifier."),
):
    """
    Create a new credential entry.
    """

    sdk = alteia_sdk()
    credentials_list = json.load(open(filepath))
    if not isinstance(credentials_list, list):
        credentials_list = [credentials_list]
    for cred in credentials_list:
        if not company and not cred.get("company", None):
            typer.secho(
                "✖ Cannot create a credential entry with the name {!r}. " "You have to define a company".format(
                    cred.get("name")
                ),
                fg=typer.colors.RED,
            )
            raise typer.Exit(2)
        elif company and not cred.get("company", None):
            cred["company"] = company
        try:
            data = {k: v for k, v in cred.items() if k not in ["name", "credentials", "company"]}
            created_cred = sdk.credentials.create(
                name=cred["name"],
                credentials=cred["credentials"],
                company=cred["company"],
                **data,
            )
            typer.secho("✓ Credentials created successfully", fg=typer.colors.GREEN)
            return created_cred
        except Exception as ex:
            print("Impossible to save {} with error {}".format(cred["name"], ex))
            raise typer.Exit(code=1)


@app.command(name="list")
def list_credentials(
    company: str = typer.Option(
        default=None,
        help="Company identifier.",
    ),
):
    """
    List the existing credentials.
    """
    sdk = alteia_sdk()
    list_filter = {}

    unique_color_company = UniqueColor()
    if company:
        list_filter.update({"company": {"$eq": company}})
    with utils.spinner():
        credentials: List[Resource] = sdk.credentials.search(filter=list_filter)  # type: ignore
    if len(credentials) > 0:
        table: Dict[str, List[str]] = init_credential_list_table()
        with utils.spinner():
            for credential in credentials:
                table["Credentials name"].append(utils.green_bold(getattr(credential, "name")))

                company_desc = utils.describe_company(sdk, getattr(credential, "company"))
                if company_desc:
                    company_name = company_desc.name
                    short_name = getattr(company_desc, "short_name", "")
                else:
                    company_name = getattr(credential, "company")
                    short_name = ""

                color_company = unique_color_company.get_colored(company_name)
                table["Company"].append(typer.style(company_name, fg=color_company, bold=True))
                table["Company shortname"].append(typer.style(short_name, fg=color_company, bold=True))
                table["Labels"].append(extract_label(credential))

        typer.secho(tabulate(table, headers="keys", tablefmt="pretty", colalign=["left"]))
    else:
        typer.secho("No credentials founds", fg=typer.colors.YELLOW)
    print()


def extract_label(credential: Resource, with_colors: bool = True) -> str:
    labels: Mapping[str, str] = getattr(credential, "labels")
    labels_formated_values: List[str] = []
    for key, value in labels.items():
        if with_colors:
            label_string = f"{utils.green_bold(key)}:{utils.blue_bold(value)}"
        else:
            label_string = f"{key}:{value}"

        labels_formated_values.append(label_string)
    return ",".join(labels_formated_values)


@app.command(name="delete")
def delete_credentials(name: str = typer.Argument(...)):
    """
    Delete a credential entry by its name.
    """
    sdk = alteia_sdk()
    found_cred = cast(
        ResourcesWithTotal,
        sdk.credentials.search(
            filter={
                "name": {"$eq": name},
            },
            return_total=True,
        ),
    )

    if found_cred.total < 1:
        typer.secho(
            "✖ Credential {!r} not found on {!r}".format(name, sdk._connection._base_url),
            fg=typer.colors.RED,
        )
        raise typer.Exit(2)

    elif found_cred.total > 1:
        credential_company = manage_delete_multi_credentials(found_cred.results)
        credential_id = [cred.id for cred in found_cred.results if cred.company == credential_company][0]
    else:
        credential_company = found_cred.results[0].company
        credential_id = found_cred.results[0].id

    try:
        sdk.credentials.delete(credential_id, company=credential_company)
    except ResponseError as e:
        typer.secho("✖ Cannot delete the credentials {!r}".format(name), fg=typer.colors.RED)
        typer.secho("details: {}".format(str(e)), fg=typer.colors.RED)
        raise typer.Exit(2)

    typer.secho("✓ Credentials {!r} deleted successfully".format(name), fg=typer.colors.GREEN)


def init_credential_list_table() -> Dict[str, List[str]]:
    table: Dict[str, List[str]] = {
        "Credentials name": [],
        "Company": [],
        "Company shortname": [],
        "Labels": [],
    }

    return table


def manage_delete_multi_credentials(credentials: List[Resource]) -> str:
    def get_credential_companies():
        choices = [cred.company for cred in credentials]
        choices.append(EXIT)

        return choices

    question = {
        "type": "list",
        "name": "company",
        "message": "which company do you want to remove the credential from?",
        "choices": get_credential_companies(),
    }
    answer = prompt(question)

    if answer["company"] == EXIT:
        typer.secho(
            "No Credential deleted",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(2)

    return answer["company"]


@app.command(name="set-credentials")
def set_credentials(
    company: str = typer.Option(default=None, help="Company identifier."),
    name: str = typer.Argument(...),
    filepath: Path = typer.Option(
        ...,  # '...' in typer.Option() makes the option required
        exists=True,
        readable=True,
        help="Path of the Credential JSON file.",
    ),
):
    """
    Set credentials.
    """

    sdk = alteia_sdk()
    with filepath.open() as file:
        credentials = json.load(file)

    try:
        response = sdk.credentials.set_credentials(name=name, company=company, credentials=credentials)
        return response
    except Exception as ex:
        print("Impossible to set credentials {} with error {}".format(name, ex))
        raise typer.Exit(code=1)


@app.command(name="set-labels")
def set_labels(
    company: str = typer.Option(default=None, help="Company identifier."),
    name: str = typer.Argument(...),
    filepath: Path = typer.Option(
        ...,  # '...' in typer.Option() makes the option required
        exists=True,
        readable=True,
        help="Path of the Labels JSON file.",
    ),
):
    """
    Set labels.
    """

    sdk = alteia_sdk()
    with filepath.open() as file:
        labels = json.load(file)

    try:
        response = sdk.credentials.set_labels(name=name, company=company, labels=labels)
        return response
    except Exception as ex:
        print("Impossible to set labels {} with error {}".format(name, ex))
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
