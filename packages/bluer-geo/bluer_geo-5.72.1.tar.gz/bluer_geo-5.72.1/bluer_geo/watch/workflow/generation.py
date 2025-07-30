from typing import List

from blueness import module
from bluer_options import string
from bluer_objects.metadata import get_from_object
from bluer_flow.workflow.generic import Workflow

from bluer_geo import NAME
from bluer_geo.watch.targets.target import Target
from bluer_geo.logger import logger

NAME = module.name(__file__, NAME)


def generate_workflow(
    algo_options: str,
    query_object_name: str,
    job_name: str,
    object_name: str,
    map_options: str,
    reduce_options: str,
) -> bool:
    list_of_datacube_id = get_from_object(
        query_object_name,
        "datacube_id",
    )

    suffix = string.pretty_date(
        include_date=False,
        as_filename=True,
        unique=True,
    )

    logger.info(
        "{}.generate_workflow @ {}: [{} X {} datacube(s)]/{}: -[{} @ {} + {}]-> {}".format(
            NAME,
            algo_options,
            query_object_name,
            len(list_of_datacube_id),
            suffix,
            map_options,
            reduce_options,
            job_name,
            object_name,
        )
    )

    workflow = Workflow(
        job_name,
        name="bluer_geo.watch",
        args={
            "algo_options": algo_options,
            "query_object_name": query_object_name,
            "object_name": object_name,
            "map_options": map_options,
            "reduce_options": reduce_options,
            "suffix": suffix,
        },
    )

    workflow.G.add_node("reduce")
    workflow.G.nodes["reduce"]["command_line"] = " ".join(
        [
            "bluer_flow_workflow monitor",
            "node=reduce",
            job_name,
            "bluer_geo_watch_reduce",
            f",{algo_options},suffix={suffix},{reduce_options}",
            query_object_name,
            object_name,
        ]
    )

    list_of_offset: List[str] = []
    for offset in range(len(list_of_datacube_id)):
        list_of_offset += [f"{offset:03d}"]

        node = f"map-{offset:03d}"

        workflow.G.add_node(node)

        workflow.G.nodes[node]["command_line"] = " ".join(
            [
                "bluer_flow_workflow monitor",
                f"node={node}",
                job_name,
                "bluer_geo_watch_map",
                f",{algo_options},offset={offset:03d},suffix={suffix},{map_options}",
                query_object_name,
            ]
        )

        workflow.G.add_edge("reduce", node)

    workflow.args["offset"] = list_of_offset

    return workflow.save()
