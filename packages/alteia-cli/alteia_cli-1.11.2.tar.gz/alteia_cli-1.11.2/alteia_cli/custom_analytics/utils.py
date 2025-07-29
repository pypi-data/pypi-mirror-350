from typing import Any, Dict, List, cast

from alteia.core.resources.resource import ResourcesWithTotal
from alteia.sdk import SDK


def get_company_id_for_shortname(sdk: SDK, short_name: str) -> None | str:
    found = cast(
        ResourcesWithTotal,
        sdk.companies.search(filter={"short_name": {"$eq": short_name}}, limit=1, return_total=True),
    )
    if found.total != 1:
        return None
    company_id = found.results[0].id
    return company_id


def get_analytics_credentials_mapping(
    sdk: SDK, company_id: str, analytics_name: str, version_range: str
) -> None | Dict[str, Any]:
    credentials_mappings = list_analytic_credentials_mappings(sdk, company_id, analytics_name)

    if not credentials_mappings:
        return None

    for cred in credentials_mappings:
        # BUG: doesn't handle equivalent version ranges like the API does
        if cred.get("analytic_version_range") == version_range:
            return cred["value"]

    return None


def list_analytic_credentials_mappings(sdk: SDK, company_id: str, analytics_name: str) -> None | List[Dict[str, Any]]:
    configuration = sdk.analytics._provider.post(
        "search-companies-analytics",
        {
            "filter": {
                "_id": {"$eq": company_id},
                "analytics.name": {"$eq": analytics_name},
            }
        },
    )

    try:
        analytics_config = next(
            filter(
                lambda ac: ac["name"] == analytics_name,
                configuration["results"][0]["analytics"],
            )
        )

        return analytics_config["credentials"]
    except (StopIteration, KeyError, IndexError):
        return None
