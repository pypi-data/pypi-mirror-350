from bluer_ai.help.generic import help_functions as generic_help_functions

from bluer_geo import ALIAS
from bluer_geo.help.catalog import help_functions as help_catalog
from bluer_geo.help.datacube import help_functions as help_datacube
from bluer_geo.help.gdal import help_functions as help_gdal
from bluer_geo.help.ingest import help_ingest
from bluer_geo.help.logger import help_log
from bluer_geo.help.QGIS import help_functions as help_QGIS
from bluer_geo.help.watch import help_functions as help_watch

help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "catalog": help_catalog,
        "datacube": help_datacube,
        "gdal": help_gdal,
        "ingest": help_ingest,
        "log": help_log,
        "QGIS": help_QGIS,
        "watch": help_watch,
    }
)
