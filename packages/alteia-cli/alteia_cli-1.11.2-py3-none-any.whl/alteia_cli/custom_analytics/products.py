from enum import Enum
from typing import Any, Dict, cast

import typer
from alteia.core.errors import ResponseError
from alteia.core.resources.resource import ResourcesWithTotal
from tabulate import tabulate

from alteia_cli import AppDesc, utils
from alteia_cli.sdk import alteia_sdk

app = typer.Typer()
app_desc = AppDesc(app, name="products", help="Interact with products.")


class ProductStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    available = "available"
    rejected = "rejected"
    failed = "failed"


def get_colored_status(status: str) -> str:
    if status == ProductStatus.available:
        colored_status = typer.style(status, fg=typer.colors.GREEN, bold=True)
    elif status in (ProductStatus.pending, ProductStatus.processing):
        colored_status = typer.style(status, fg=typer.colors.YELLOW, bold=True)
    elif status in (ProductStatus.rejected, ProductStatus.failed):
        colored_status = typer.style(status, fg=typer.colors.RED, bold=True)
    else:
        colored_status = status
    return colored_status


@app.command(name="list")
def list_products(
    limit: int = typer.Option(10, "--limit", "-n", min=1, help="Max number of products returned", show_default=True),
    analytic: str = typer.Option(default=None, help="Analytic name"),
    company: str = typer.Option(default=None, help="Company identifier"),
    status: ProductStatus = typer.Option(default=None, case_sensitive=False, help="Product status"),
    display_all: bool = typer.Option(
        False,
        "--all",
        case_sensitive=False,
        help="If set, display also the products from platform analytics "
        "(otherwise only products from custom analytics are displayed).",
    ),
):
    """List the products"""
    sdk = alteia_sdk()
    search_filter: Dict[str, Any]
    search_filter = {
        "parent_workflow": {"$exists": False},
    }
    if not display_all:
        search_filter.update({"analytic.external": {"$eq": True}})
    if analytic:
        search_filter.update({"analytic.name": {"$eq": analytic}})
    if company:
        search_filter.update({"company": {"$eq": company}})
    if status:
        search_filter.update({"status": {"$eq": status}})
    with utils.spinner():
        found_products = cast(
            ResourcesWithTotal,
            sdk.products.search(filter=search_filter, return_total=True, limit=limit, sort={"creation_date": -1}),
        )
        results = found_products.results

    if len(results) > 0:
        progress_list = []
        for r in results:
            if hasattr(r, "progress"):
                progress_list.append(str(r.progress) + "%")
            else:
                progress_list.append("-")

        table = {
            "Product name": [typer.style(r.name, fg=typer.colors.GREEN, bold=True) for r in results],
            "Status": [get_colored_status(r.status) for r in results],
            "Progress": progress_list,
            "Creation date": [r.creation_date for r in results],
            "Identifier": [r.id for r in results],
        }
        typer.secho(tabulate(table, headers="keys", tablefmt="pretty", colalign=("left", "left")))
        print()
        print("{}/{} products displayed".format(len(results), found_products.total))

    else:
        print("No product found.")


def get_colored_levelname(levelname: str) -> str:
    if levelname.upper() == "INFO":
        colored_levelname = typer.style(levelname, bold=True)
    elif levelname.upper() == "WARNING":
        colored_levelname = typer.style(levelname, fg=typer.colors.YELLOW, bold=True)
    elif levelname.upper() in ("ERROR", "CRITICAL"):
        colored_levelname = typer.style(levelname, fg=typer.colors.RED, bold=True)
    else:
        colored_levelname = levelname
    return colored_levelname


def format_log(log):
    d = log.timestamp
    formatted_timestamp = d.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Display only ms
    message = log.record.get("message").strip()
    if log.record.get("levelname") != "DEBUG":
        message = typer.style(message, bold=True)

    return "{date} {level}\t {message}".format(
        date=formatted_timestamp,
        level=get_colored_levelname(log.record.get("levelname")),
        message=message,
    )


@app.command()
def cancel(product_id: str = typer.Argument(...)):
    """
    Cancel a running product.
    """
    sdk = alteia_sdk()

    try:
        sdk.products.cancel(product_id)
        print("Product canceled")
    except ResponseError as e:
        typer.secho("✖ Cannot cancel product {!r}".format(product_id), fg=typer.colors.RED)
        typer.secho("details: {}".format(str(e)), fg=typer.colors.RED)
        raise typer.Exit(2)


@app.command()
def logs(
    product_id: str = typer.Argument(...), follow: bool = typer.Option(False, "--follow", "-f", help="Follow logs.")
):
    """
    Retrieve the logs of a product.
    """
    sdk = alteia_sdk()

    _product_id = product_id

    try:
        if follow:
            print("[Follow mode] Press <Ctrl-C> to quit")
            for log in sdk.products.follow_logs(_product_id):
                typer.secho(format_log(log))

        else:
            for log in sdk.products.retrieve_logs(_product_id).logs:
                typer.secho(format_log(log))
    except ResponseError as e:
        typer.secho("✖ Cannot retrieve logs for the product {!r}".format(product_id), fg=typer.colors.RED)
        typer.secho("details: {}".format(str(e)), fg=typer.colors.RED)
        raise typer.Exit(2)


if __name__ == "__main__":
    app()
