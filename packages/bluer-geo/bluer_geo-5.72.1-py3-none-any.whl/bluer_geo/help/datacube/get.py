from typing import List

from bluer_options.terminal import show_usage


def help_get(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "catalog | raw | template"

    return show_usage(
        [
            "@datacube get",
            f"[{options}]",
            "[.|<datacube-id>]",
        ],
        "get datacube properties.",
        mono=mono,
    )
