import os

from qgis.core import *
from qgis.gui import *


@qgsfunction(args="auto", group="Custom", referenced_columns=[])
def vanwatch_display(layer_filename, cameras, feature, parent):
    """
    Produce display text for a vanwatch mapid.

    vanwatch_display(
        layer_property(@layer,'path'),
        "cameras"
    )
    """
    version = "5.16.1"

    layer_path = os.sep.join(layer_filename.split(os.sep)[:-1])
    object_name = layer_filename.split(os.sep)[-2]

    image_name_list = [url.split("/")[-1].split(".")[0] for url in cameras.split(",")]

    image_filename_list = [
        "file://{}/{}-inference.jpg".format(
            layer_path,
            image_name,
        )
        for image_name in image_name_list
    ]

    image_tag_list = [
        f'<a href="{image_filename}"><img src="{image_filename}" alt="{image_filename}" height=100 ></a>'
        for image_filename in image_filename_list
    ]

    return "\n".join(
        [
            '<table border="1">',
            "    <tr>",
        ]
        + [f"        <td>{image_tag}</td>" for image_tag in image_tag_list]
        + [
            "    </tr>",
            "</table>",
        ]
        + [
            '<p style="color: white; width: 500px">{}</p>'.format(
                " | ".join(
                    [
                        object_name,
                        "🌈 Vancouver Watching",
                        f"template-{version}",
                    ]
                )
            )
        ]
    )
