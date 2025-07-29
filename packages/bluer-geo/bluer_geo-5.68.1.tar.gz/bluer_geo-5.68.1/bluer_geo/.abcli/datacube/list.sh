#! /usr/bin/env bash

function bluer_geo_datacube_list() {
    local datacube_id=$(bluer_ai_clarify_object $1 .)

    python3 -m bluer_geo.datacube \
        list \
        --datacube_id $datacube_id \
        "${@:2}"
}
