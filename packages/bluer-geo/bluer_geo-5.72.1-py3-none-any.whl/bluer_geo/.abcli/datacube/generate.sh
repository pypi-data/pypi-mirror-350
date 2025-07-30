#! /usr/bin/env bash

function bluer_geo_datacube_generate() {
    local options=$1
    local dryrun=$(bluer_ai_option_int "$options" dryrun 0)

    local datacube_id=$(bluer_ai_clarify_object $2 .)

    local command=$(python3 -m bluer_geo.datacube \
        generate \
        --datacube_id $datacube_id \
        "${@:3}")

    bluer_ai_eval dryrun=$dryrun \
        "$command"
}
