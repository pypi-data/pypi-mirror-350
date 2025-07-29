import os

from bluer_options import MARQUEE as default_MARQUEE
from bluer_options.help.functions import get_help
from bluer_objects import file, README

from bluer_geo.catalog.README import build as build_catalog
from bluer_geo.watch.README import items as watch_items, macros as watch_macros
from bluer_geo.objects.README import build as build_objects
from bluer_geo.watch.targets.README import build as build_targets
from bluer_geo.help.functions import help_functions
from bluer_geo import NAME, VERSION, ICON, REPO_NAME


items = README.Items(
    [
        {
            "name": "Maxar Open Data",
            "description": "catalog: [Maxar's Open Data program](https://www.maxar.com/open-data/)",
            "marquee": "https://github.com/kamangir/assets/blob/main/blue-geo/MaxarOpenData.png?raw=true",
            "url": "./bluer_geo/catalog/maxar_open_data",
        },
        {
            "name": "copernicus",
            "description": "catalog: [Copernicus Data Space Ecosystem - Europe's eyes on Earth](https://dataspace.copernicus.eu/)",
            "marquee": "https://github.com/kamangir/assets/blob/main/blue-geo/copernicus.jpg?raw=true",
            "url": "./bluer_geo/catalog/copernicus",
        },
        {
            "name": "firms-area",
            "description": "catalog: Fire Information for Resource Management System ([FIRMS](https://firms.modaps.eosdis.nasa.gov)).",
            "marquee": "https://github.com/kamangir/assets/blob/main/blue-geo/datacube-firms_area.jpg?raw=true",
            "url": "./bluer_geo/catalog/firms",
        },
        {
            "name": "ukraine-timemap",
            "description": "catalog: [Bellingcat](https://www.bellingcat.com/) [Civilian Harm in Ukraine TimeMap](https://github.com/bellingcat/ukraine-timemap) dataset, available through [this UI](https://ukraine.bellingcat.com/) and [this API](https://bellingcat-embeds.ams3.cdn.digitaloceanspaces.com/production/ukr/timemap/api.json).",
            "marquee": "https://github.com/kamangir/assets/blob/main/nbs/ukraine-timemap/QGIS.png?raw=true",
            "url": "./bluer_geo/catalog/ukraine_timemap",
        },
        {
            "name": "QGIS",
            "description": "An AI terraform for [QGIS](https://www.qgis.org/).",
            "marquee": "https://github.com/kamangir/assets/blob/main/blue-geo/QGIS.jpg?raw=true",
            "url": "./bluer_geo/QGIS/README.md",
        },
        {
            "name": "global-power-plant-database",
            "description": "The Global Power Plant Database is a comprehensive, open source database of power plants around the world [datasets.wri.org](https://datasets.wri.org/datasets/global-power-plant-database).",
            "marquee": "https://github.com/kamangir/assets/blob/main/blue-geo/global_power_plant_database-cover.png?raw=true",
            "url": "./bluer_geo/objects/md/global_power_plant_database.md",
        },
        {
            "name": "geo-watch",
            "description": "Watch the planet's story unfold.",
            "marquee": "https://github.com/kamangir/assets/blob/main/blue-geo/blue-geo-watch.png?raw=true",
            "url": "./bluer_geo/watch",
        },
        {
            "name": "catalog",
            "description": "Generalized STAC Catalogs.",
            "marquee": default_MARQUEE,
            "url": "./bluer_geo/catalog",
        },
        {
            "name": "datacube",
            "description": "Generalized STAC Items.",
            "marquee": default_MARQUEE,
            "url": "./bluer_geo/datacube",
        },
    ]
)


def build() -> bool:
    return (
        build_catalog()
        and build_targets()
        and build_objects()
        and all(
            README.build(
                items=items,
                cols=cols,
                path=os.path.join(file.path(__file__), suffix),
                macros=macros,
                ICON=ICON,
                NAME=NAME,
                VERSION=VERSION,
                REPO_NAME=REPO_NAME,
                help_function=lambda tokens: get_help(
                    tokens,
                    help_functions,
                    mono=True,
                ),
            )
            for suffix, items, cols, macros, in [
                ("..", items, 3, {}),
                ("catalog", [], -1, {}),
                ("datacube", [], -1, {}),
                ("watch", watch_items, -1, watch_macros),
                ("QGIS", [], -1, {}),
            ]
        )
    )
