import itertools
import json
import pprint
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import alteia
import click_spinner
import jsonschema
import typer
import yaml
from alteia.core.errors import ResponseError
from alteia.core.resources.resource import Resource
from alteia.core.utils.typing import ResourceId

# Replace default spinner with a prettier
SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
click_spinner.Spinner.spinner_cycle = itertools.cycle(SPINNER)


def spinner():
    return click_spinner.spinner()


def validate_against_schema(instance: Union[Dict, List], *, json_schema: Dict):
    """Validate the given instance (object representation of a JSON string).

    Args:
        instance: The instance to validate.

        json_schema: JSON schema dict.

    """
    v = jsonschema.Draft7Validator(json_schema)
    errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
    if errors:
        reason = __create_validation_error_msg(errors)
        return reason
    else:
        return None


def __create_validation_error_msg(errors):
    error_msgs = []
    for error in errors:
        path = [str(sub_path) for sub_path in error.path]
        str_path = ""
        if path:
            str_path = "#/{}: ".format("/".join(path))
        error_msg = " - {}{}".format(str_path, error.message)
        error_msgs.append(error_msg)
    return "\n".join(error_msgs)


def check_json_schema(json_schema):
    if not json_schema:
        return

    try:
        jsonschema.Draft7Validator(json_schema).check_schema(json_schema)
    except jsonschema.SchemaError as e:
        typer.secho("✖ Invalid JSON schema:\n{}".format(pprint.pformat(json_schema, indent=2)), fg=typer.colors.RED)
        typer.secho("\ndetails: {}".format(e.message), fg=typer.colors.RED)
        raise typer.Exit(2)


@lru_cache(maxsize=32)
def describe_company(sdk: alteia.SDK, company_id: ResourceId) -> Optional[Resource]:
    try:
        return sdk.companies.describe(company_id)
    except ResponseError:
        return None


def green_bold(s: str):
    return typer.style(s, fg=typer.colors.GREEN, bold=True)


def blue_bold(s: str):
    return typer.style(s, fg=typer.colors.CYAN, bold=True)


def get_file_contents(file_path: Union[str, Path]) -> str:
    with open(file_path, "r", encoding="utf-8") as handler:
        return handler.read()


def load_yaml_contents(str_contents: str) -> Dict:
    return yaml.load(str_contents, Loader=yaml.Loader)


def load_yaml_file(file_path: Union[str, Path]) -> Dict:
    return load_yaml_contents(get_file_contents(file_path))


def dump_yaml(any_data: Any) -> str:
    return yaml.dump(any_data, indent=2, allow_unicode=True, sort_keys=False)


def load_json_file(file_path: Union[str, Path]) -> Dict:
    return json.loads(get_file_contents(file_path))


def dump_pretty_json(any_data: Any) -> str:
    return json.dumps(any_data, indent=4)


def print_ok(msg: str, check=True):
    if check:
        msg = f"✓ {msg}"
    typer.secho(msg, fg=typer.colors.GREEN)


def print_warn(msg: str, check=True):
    if check:
        msg = f"⚠ {msg}"
    typer.secho(msg, fg=typer.colors.YELLOW)


def print_error(msg: str, check=True, raise_exit=False):
    if check:
        msg = f"✖ {msg}"
    typer.secho(msg, fg=typer.colors.RED)
    if raise_exit:
        raise typer.Exit(1)
