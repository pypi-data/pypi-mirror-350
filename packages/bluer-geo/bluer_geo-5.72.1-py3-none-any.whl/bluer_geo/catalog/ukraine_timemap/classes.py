from blueness import module
from bluer_geo import NAME
from bluer_geo.catalog.generic import GenericCatalog
from bluer_geo.logger import logger

NAME = module.name(__file__, NAME)


class UkraineTimemapCatalog(GenericCatalog):
    name = "ukraine_timemap"

    url = {
        "home": "https://ukraine.bellingcat.com/",
        "dataset": "https://bellingcat-embeds.ams3.cdn.digitaloceanspaces.com/production/ukr/timemap/api.json",
        "github": "https://github.com/bellingcat/ukraine-timemap",
    }
