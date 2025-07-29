from typing import List

from bluer_options.terminal import show_usage

from bluer_geo.catalog import get_catalog

from bluer_geo.catalog.classes import list_of_catalogs


def help_browse(
    tokens: List[str],
    mono: bool,
) -> str:
    if tokens:
        catalog_name = tokens[0]
        catalog = get_catalog(catalog_name)

        return show_usage(
            [
                "@catalog browse",
                catalog_name,
                "|".join(catalog.url.keys()),
            ],
            f"browse {catalog_name}.",
            mono=mono,
        )

    return "\n".join([help_browse([catalog], mono) for catalog in list_of_catalogs])
