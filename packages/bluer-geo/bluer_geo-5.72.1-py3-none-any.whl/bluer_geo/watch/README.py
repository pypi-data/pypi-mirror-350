from typing import List, Dict
import os

from bluer_options import string
from bluer_objects import file
from bluer_geo.watch.targets.target_list import TargetList
from bluer_geo.watch.targets.Miduk import README as Miduk


list_of_targets = {
    "Miduk": Miduk,
}

targets_path = file.path(__file__)

items: List[str] = []
for target_name in sorted(list_of_targets.keys()):
    target_info = list_of_targets[target_name]

    list_of_objects = target_info["objects"]
    assert isinstance(list_of_objects, dict)

    target_README = f"./targets/md/{target_name}.md"

    target_title = "`{}`".format(target_info.get("title", target_name))

    items += [
        (
            f"## [{target_title}]({target_README})"
            if file.exists(os.path.join(targets_path, target_README))
            else f"## {target_title}"
        ),
    ]

    target_list = TargetList()

    if list_of_objects:
        thumbnail_info = target_info.get("thumbnail", {})
        assert isinstance(thumbnail_info, dict)

        thumbnail_index = thumbnail_info.get("index", -1)

        thumbnail_scale = thumbnail_info.get("scale", 2)
        thumbnail_scale_str = f"-{thumbnail_scale}X" if thumbnail_scale != 1 else ""

        thumbnail_object_name = list(list_of_objects.keys())[thumbnail_index]

        thumbnail_url = f"TBA/{thumbnail_object_name}/{thumbnail_object_name}.gif"

        thumbnail_scale_url = f"TBA/{thumbnail_object_name}/{thumbnail_object_name}{thumbnail_scale_str}.gif"

        items += [
            "",
            "<details>",
            "<summary>🌐</summary>",
            "",
            f"[![image]({thumbnail_scale_url}?raw=true&random={string.random()})]({thumbnail_url})",
            "",
            "</details>",
            "",
        ]

    items += target_list.get(
        target_info.get(
            "target_name",
            target_name,
        )
    ).urls_as_str()

    items += [
        "- {}.".format(
            ", ".join(
                [
                    f"[`{object_name}`](TBA/{object_name}.tar.gz)",
                    f"[gif](TBA/{object_name}/{object_name}.gif)",
                ]
                + description
            )
        )
        for object_name, description in list_of_objects.items()
    ]

    items += [""]

macros: Dict[str, str] = {
    "--scale-note--": [
        "ℹ️ suffix published gif urls with `-2X` and `-4X` for different scales."
    ]
}
