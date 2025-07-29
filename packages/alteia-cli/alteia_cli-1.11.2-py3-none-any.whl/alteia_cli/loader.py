import importlib.util
import inspect
import logging
import pkgutil
import sys
from typing import Iterable, List

import typer

from alteia_cli import AppDesc

LOGGER = logging.getLogger(__name__)


def _is_app_desc(obj):
    """Check whether object is an instance of AppDesc."""
    return isinstance(obj, AppDesc)


def _discover(submodules_path: Iterable[str]) -> List[AppDesc]:
    """Import submodules and build list of app descriptions."""
    found = []
    LOGGER.debug(f"Searching for app descriptions in {submodules_path!r}")
    for loader, modname, _ in pkgutil.walk_packages(submodules_path):
        modspec = loader.find_spec(modname, None)
        if modspec is None or modspec.loader is None:
            continue
        mod = importlib.util.module_from_spec(modspec)
        # add module to sys modules so that the module can be imported by name
        # needed because of the way analytics modules loads its yaml schema
        sys.modules[modname] = mod
        modspec.loader.exec_module(mod)
        apps = inspect.getmembers(mod, _is_app_desc)
        for _, obj in apps:
            found.append(obj)

    LOGGER.debug(f"Found {len(found)} app descriptions")
    return found


class Loader:
    def __init__(self, app: typer.Typer):
        self._app = app
        self._app_names: List[str] = []

    def extend_app(self, submodules_path: Iterable[str]):
        found = _discover(submodules_path)
        for app_desc in found:
            app_name = app_desc.name

            if app_name in self._app_names:
                typer.secho(f"Found an application conflict for {app_name!r}", fg=typer.colors.RED)
                continue

            LOGGER.debug(f"Adding {app_name!r} app")
            self._app.add_typer(app_desc.app, name=app_name, help=app_desc.help)
            self._app_names.append(app_name)
