import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from bluer_geo import NAME
from bluer_geo.catalog.ukraine_timemap.ukraine_timemap.classes import (
    UkraineTimemapDatacube,
)
from bluer_geo.logger import logger

NAME = module.name(__file__, NAME)


parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="query",
)
parser.add_argument(
    "--object_name",
    type=str,
)
args = parser.parse_args()

success = False
if args.task == "query":
    success = UkraineTimemapDatacube.query(object_name=args.object_name)
else:
    success = None

sys_exit(logger, NAME, args.task, success)
