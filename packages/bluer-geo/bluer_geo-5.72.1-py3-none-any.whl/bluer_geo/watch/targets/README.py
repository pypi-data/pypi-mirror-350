import os

from bluer_options.help.functions import get_help
from bluer_objects import file, README

from bluer_geo import NAME, VERSION, ICON, REPO_NAME
from bluer_geo.help.functions import help_functions
from bluer_geo.watch.targets.target_list import TargetList


def build() -> bool:
    target_list = TargetList(download=True)

    return all(
        README.build(
            items=items,
            cols=cols,
            path=os.path.join(
                file.path(__file__),
                f"md/{suffix}",
            ),
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
            (
                f"{target_name}.md",
                [],
                3,
                {
                    "--footer--": [
                        "---",
                        "",
                        "used by: {}.".format(
                            ", ".join(
                                sorted(
                                    [
                                        "[`@geo watch`](../../)",
                                    ]
                                )
                            )
                        ),
                    ],
                    "--urls--": target_list.get(target_name).urls_as_str(),
                },
            )
            for target_name in [
                "Miduk",
            ]
        ]
    )
