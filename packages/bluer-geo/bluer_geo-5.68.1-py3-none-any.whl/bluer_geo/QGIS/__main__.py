import argparse

from blueness import module
from blueness.argparse.generic import sys_exit
from bluer_objects.env import ABCLI_OBJECT_ROOT

from bluer_geo import NAME
from bluer_geo.QGIS.seed import generate_seed, default_init_script
from bluer_geo.QGIS.dependency import list_of_dependencies
from bluer_geo.logger import logger

NAME = module.name(__file__, NAME)

list_of_tasks = "generate_seed|list_dependencies"

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help=list_of_tasks,
)
parser.add_argument(
    "--delim",
    type=str,
    default="+",
)
parser.add_argument(
    "--filename",
    type=str,
)
parser.add_argument(
    "--verbose",
    type=int,
    default="0",
    help="0|1",
)
parser.add_argument(
    "--init_script",
    type=str,
    default="+".join(default_init_script),
    help=" + ".join(default_init_script),
)
args = parser.parse_args()

delim = " " if args.delim == "space" else args.delim

success = args.task in list_of_tasks.split("|")
if args.task == "generate_seed":
    print(
        generate_seed(
            init_script=args.init_script.split("+"),
        )
    )
elif args.task == "list_dependencies":
    output = list_of_dependencies(
        filename=args.filename,
        ABCLI_OBJECT_ROOT=ABCLI_OBJECT_ROOT,
        verbose=args.verbose == 1,
    )

    print(delim.join(output))
else:
    success = None

sys_exit(logger, NAME, args.task, success)
