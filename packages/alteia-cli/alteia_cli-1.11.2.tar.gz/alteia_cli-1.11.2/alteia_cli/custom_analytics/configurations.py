from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

import typer
from alteia.core.errors import ResponseError
from alteia.core.resources.resource import ResourcesWithTotal
from tabulate import tabulate

from alteia_cli import AppDesc
from alteia_cli.sdk import alteia_sdk
from alteia_cli.utils import (
    blue_bold,
    dump_pretty_json,
    dump_yaml,
    green_bold,
    load_json_file,
    load_yaml_file,
    print_error,
    print_ok,
    spinner,
)

app = typer.Typer()
app_desc = AppDesc(app, name="analytic-configurations", help="Interact with configurations of analytics.")


def _explode_versions_for_list(versions: List[dict]) -> str:
    """
    return one string containing as many lines as versions.
    Each line has the analytic version range + nb properties of the value
    """
    # versions = sorted(versions, key=lambda v: v['analytic_version_range'])
    txt = [f'{v["analytic_version_range"]:>12} [{len(v["value"]):3} properties]' for v in versions]
    return "\n".join(txt)


def _get_ranges_from_versions(versions: List[dict]) -> List[str]:
    """return list of version ranges existing in versions list"""
    return [v["analytic_version_range"] for v in versions]


def _get_version_from_range(versions: List[dict], wanted_range: str) -> Optional[dict]:
    """return the version where analytic_version_range matches the wanted range"""
    return next((v for v in versions if v["analytic_version_range"] == wanted_range), None)


class ConfigFileFormat(str, Enum):
    json = "json"
    yaml = "yaml"


@app.command(name="list")
def list_configurations(
    limit: int = typer.Option(100, "--limit", "-n", min=1, help="Max number of configuration sets returned."),
    name: str = typer.Option(default=None, help="Configuration set name (or a part of) to match"),
    analytic: str = typer.Option(default=None, help="Exact analytic name to match"),
    desc: bool = typer.Option(False, "--desc", help="Print description rather than configurations"),
    domain: str = typer.Option(default=None, hidden=True),
    ids: str = typer.Option(default=None, hidden=True),
):
    """
    List the analytic configuration sets and their configurations.
    """
    sdk = alteia_sdk()
    search_filter: Dict[str, Dict[str, Any]] = {}
    if name:
        search_filter["name"] = {"$match": name}
    if analytic:
        search_filter["analytic_name"] = {"$eq": analytic}
    if domain:
        search_filter["domain"] = {"$eq": domain}
    if ids:
        search_filter["_id"] = {"$in": ids.split(",")}

    with spinner():
        configs = cast(
            ResourcesWithTotal,
            sdk.analytic_configurations.search(
                filter=search_filter, return_total=True, limit=limit, sort={"creation_date": -1}
            ),
        )

    if len(configs.results) == 0:
        print("No analytic configuration set found.")
        return

    table: Dict[str, List[str]] = {
        "Configuration set Identifier": [],
        "Configuration set Name": [],
        "Analytic name": [],
    }
    if desc:
        table["Description"] = []
        # table['Revision'] = []
        col_align = ["left", "left", "left", "left"]
        max_col_widths = [24, 40, 40, 40]
    else:
        table["NB configurations"] = []
        table["Applied range + config size"] = []
        col_align = ["left", "left", "left", "center", "right"]
        max_col_widths = [24, 40, 40, 5, 30]

    for config in configs.results:
        table["Configuration set Identifier"].append(config.id)
        table["Configuration set Name"].append(green_bold(config.name))
        table["Analytic name"].append(blue_bold(config.analytic_name))
        if desc:
            table["Description"].append(getattr(config, "description", ""))
            # table['Revision'].append(str(config.revision))
        else:
            table["NB configurations"].append(str(len(config.versions)))
            config_stats = _explode_versions_for_list(config.versions)
            table["Applied range + config size"].append(config_stats)

    typer.secho(
        tabulate(
            table,
            headers="keys",
            tablefmt="pretty",
            colalign=col_align,
            maxcolwidths=max_col_widths,
        )
    )

    print()
    print(f"{len(configs.results)}/{configs.total} configurations displayed")


def _load_config_file(file_path: Path) -> Dict:
    """load the config file and return a dictionary, could be a json or yaml file"""
    contents = {}
    try:
        if file_path.suffix.lower() in (".yml", ".yaml"):
            contents = load_yaml_file(file_path)
        else:  # assume it's a json
            contents = load_json_file(file_path)
    except Exception as err:
        # could be any file error: json, yaml, file existence, read error, etc.
        print_error(f'Something is wrong with this file "{file_path}": {err}', raise_exit=True)
    return contents


@app.command()
def create(
    config_path: Path = typer.Option(
        ...,
        "--config-path",
        "-c",
        exists=True,
        readable=True,
        help="Path to the Configuration file (YAML or JSON file)",
    ),
    name: str = typer.Option(None, "--name", "-n", help="Configuration set name (will be prompt if not provided)"),
    analytic: str = typer.Option(None, "--analytic", "-a", help="Analytic name (will be prompt if not provided)"),
    analytic_version_range: str = typer.Option(
        None,
        "--version-range",
        "-v",
        help="Version range of the analytic on which " "this first configuration can be applied",
    ),
    description: str = typer.Option(None, "--description", "-d", help="Configuration set description text"),
    domain: str = typer.Option(None, hidden=True),
):
    """
    Create a new configuration set for an analytic.

    A configuration set is composed of configurations, each being applied to
    a different version range of the associated analytic.
    """
    config_desc = _load_config_file(config_path)
    print(f"Configuration file is loaded: {config_path}")

    if name is None:
        name = typer.prompt(typer.style("Required configuration set name", bold=True))
    if analytic is None:
        analytic = typer.prompt(typer.style("Required Analytic name", bold=True))

    sdk = alteia_sdk()

    create_kwargs: Dict[str, str] = {}
    if analytic_version_range is not None:
        create_kwargs["analytic_version_range"] = analytic_version_range
    if description is not None:
        create_kwargs["description"] = description
    if domain is not None:
        create_kwargs["domain"] = domain

    try:
        new_config = sdk.analytic_configurations.create(
            name=name,
            analytic_name=analytic,
            value=config_desc,
            **create_kwargs,
        )
        print_ok(f"Configuration set created successfully: {new_config.id}")
    except ResponseError as err:
        print_error(
            f'Cannot create the configuration set "{name}" ' f'for the analytic "{analytic}"\n' f"Details: {err}",
            raise_exit=True,
        )


@app.command()
def delete(
    ids: str = typer.Argument(
        ...,
        help="Identifier of the configuration set to delete, or "
        "comma-separated list of configuration set identifiers",
    ),
):
    """
    Delete one or many analytic configuration set(s)
    and the associated configuration(s).
    """
    list_ids = ids.split(",")
    sdk = alteia_sdk()
    try:
        sdk.analytic_configurations.delete(list_ids)
        print_ok(f"Configuration set(s) deleted successfully: {list_ids}")
    except ResponseError as err:
        print_error(f"Cannot delete configuration set(s): {list_ids}\n" f"Details: {err}", raise_exit=True)


@app.command()
def update(
    config_set_id: str = typer.Argument(..., help="Identifier of the configuration set to update"),
    name: str = typer.Option(None, "--name", "-n", help="New configuration set name"),
    description: str = typer.Option(None, "--description", "-d", help="New configuration set description"),
    add_config: Path = typer.Option(
        None,
        "--add-config",
        "-a",
        exists=True,
        readable=True,
        help="Add new configuration. Specify the path to the new configuration file, "
        "and --version-range option with the version range of the analytic you "
        "want this new configuration to be applied. "
        "Do not use with --replace-config",
    ),
    replace_config: Path = typer.Option(
        None,
        "--replace-config",
        "-u",
        exists=True,
        readable=True,
        help="Replace a configuration. Specify the path to the new configuration "
        "file, and --version-range option with the exact version range from "
        "the applicable analytic version ranges. "
        "Do not use with --add-config",
    ),
    version_range: str = typer.Option(
        None,
        "--version-range",
        "-v",
        help="Version range of the analytic on which a configuration can be "
        "applied. Must be used with one of --add-config, "
        "--replace-config or --remove-config",
    ),
    remove_config: str = typer.Option(
        None,
        "--remove-config",
        "-r",
        help="Remove a configuration. Specify the exact version range from " "the applicable analytic version ranges",
    ),
):
    """
    Update a configuration set.
    A configuration set is composed of configurations, each being applied
    to a different version range of the associated analytic.

    To add a new configuration (file), use --add-config with the path to the new
    configuration file (YAML or JSON file) and --version-range with the version range
    of the analytic you want this new configuration to be applied.

    To replace an existing configuration (file), use --replace-config with the path
    to the new configuration file (YAML or JSON file) and --version-range with the
    exact version range attached to the configuration to replace.

    To remove a configuration from a configuration set, use --remove-config
    and --version-range with the exact version range attached to the configuration
    to remove.

    To change the version range for an existing configuration, do an "add" and then
    a "remove" (an export may be necessary to do the "add" with the same
    configuration file).
    """

    sdk = alteia_sdk()

    try:
        found_config = sdk.analytic_configurations.describe(config_set_id)
        config_versions = found_config.versions
        update_versions = False
        available_ranges = _get_ranges_from_versions(config_versions)

        updates: Dict[str, Any] = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description

        # do remove version
        if remove_config:
            found_version = _get_version_from_range(config_versions, remove_config)
            if found_version is None:
                print_error(
                    f"Configuration with analytic version range "
                    f'equals to "{remove_config}" does not exist in '
                    f"the configuration set.\n"
                    f"Existing version ranges: {available_ranges}.",
                    raise_exit=True,
                )
            config_versions.remove(found_version)
            update_versions = True

        # cannot use add and replace at the same time
        if replace_config and add_config:
            print_error('Cannot use ate the same time "--add-config" and ' '"--replace-config".', raise_exit=True)

        # for add and replace, version_range is mandatory
        if (replace_config or add_config) and version_range is None:
            print_error('"--version-range" is required to add or replace a config.', raise_exit=True)

        # replace value
        if replace_config:
            found_version = _get_version_from_range(config_versions, version_range)
            if found_version is None:
                print_error(
                    f"Configuration version with analytic version range "
                    f'equals to "{version_range}" does not exist in '
                    f"the versions list.\n"
                    f"Existing version ranges: {available_ranges}.",
                    raise_exit=True,
                )
            else:
                # this changes the value by reference in config_versions:
                found_version["value"] = _load_config_file(replace_config)
                update_versions = True

        # add version
        if add_config:
            config_versions.append({"analytic_version_range": version_range, "value": _load_config_file(add_config)})
            update_versions = True

        if update_versions:
            updates["versions"] = config_versions

        updated_config = sdk.analytic_configurations.update(
            config_set_id,
            **updates,
        )
        print_ok(f"Configuration set updated successfully: {updated_config.id}")
    except ResponseError as err:
        print_error(f'Cannot update the configuration set "{config_set_id}"\n' f"Details: {err}", raise_exit=True)


@app.command(name="export")
def export_value(
    config_set_id: str = typer.Argument(..., help="Identifier of the configuration set to export value"),
    version_range: str = typer.Option(
        None,
        "--version-range",
        "-v",
        help="Specify the exact version range from the applicable analytic version "
        "ranges. Optional if only one configuration exists in the "
        "configuration set",
    ),
    export_format: ConfigFileFormat = typer.Option(
        ConfigFileFormat.json.value, "--format", "-f", case_sensitive=False, help="Optional output format"
    ),
    output_path: Path = typer.Option(
        None,
        "--output-path",
        "-o",
        exists=False,
        writable=True,
        help="Optional output filepath to export the configuration. "
        "If the filepath already exists, it will be replaced. "
        "If not specified, configuration will be displayed in stdout",
    ),
):
    """
    Export one configuration of a configuration set.
    Output can be a JSON or YAML format.
    """
    sdk = alteia_sdk()
    try:
        found_config = sdk.analytic_configurations.describe(config_set_id)
        config_versions = found_config.versions
        available_ranges = _get_ranges_from_versions(config_versions)

        if version_range is None:
            if len(config_versions) > 1:
                print_error(
                    f"{len(config_versions)} configurations found in the "
                    f'configuration set "{config_set_id}". '
                    f"A version range must be specified: {available_ranges}.",
                    raise_exit=True,
                )
            found_version = config_versions[0]
        else:
            found_version = _get_version_from_range(found_config.versions, version_range)

        contents = ""
        if found_version is None:
            print_error(
                f"Configuration with analytic version range equals to "
                f'"{version_range}" does not exist in the '
                f'configuration set "{config_set_id}".\n'
                f"Existing version ranges: {available_ranges}.",
                raise_exit=True,
            )
        elif export_format == ConfigFileFormat.json:
            contents = dump_pretty_json(found_version["value"])
        elif export_format == ConfigFileFormat.yaml:
            contents = dump_yaml(found_version["value"])

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(contents)
        else:
            print(contents)

    except ResponseError as err:
        print_error(
            f"Cannot export a configuration applied to "
            f'version range "{version_range}" from '
            f'the configuration set "{config_set_id}".\n'
            f"Details: {err}",
            raise_exit=True,
        )


@app.command(name="assign")
def assign_to_company(
    config_set_id: str = typer.Argument(..., help="Identifier of the configuration set to assign"),
    company_id: str = typer.Option(
        ..., "--company", "-c", help="Identifier of the company the configuration set will be assigned to"
    ),
):
    """
    Assign an analytic configuration set to a company.

    All analytic configurations that are currently part of this
    analytic configuration set (and the potential future ones),
    are assigned to the company.
    """
    sdk = alteia_sdk()

    try:
        company = sdk.companies.describe(company_id)
        result = sdk.analytic_configurations.assign_to_company(
            config_set_id,
            company=company.id,
        )
        company_name = getattr(company, "name", "unknown")
        print_ok(
            f'Configuration set "{config_set_id}" successfully assigned '
            f'to company "{result.get("company")}" ({company_name})'
        )
    except ResponseError as err:
        print_error(
            f"Cannot assign configuration {config_set_id} " f"to company {company_id}\n" f"Details: {err}",
            raise_exit=True,
        )


@app.command(name="unassign")
def unassign_from_company(
    config_set_id: str = typer.Argument(..., help="Identifier of the configuration set to unassign"),
    company_id: str = typer.Option(
        ..., "--company", "-c", help="Identifier of the company the configuration set is assigned to"
    ),
):
    """
    Unassign an analytic configuration set from a company.

    All configurations currently part of this analytic configuration set,
    are unassigned from the company.
    """
    sdk = alteia_sdk()

    try:
        sdk.analytic_configurations.unassign_from_company(
            config_set_id,
            company=company_id,
        )
        print_ok(f'Configuration set "{config_set_id}" successfully unassigned ' f'from company "{company_id}"')
    except ResponseError as err:
        print_error(
            f'Cannot unassign configuration set "{config_set_id}" ' f'from company "{company_id}"\n' f"Details: {err}",
            raise_exit=True,
        )
