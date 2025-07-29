#! /usr/bin/env bash

function bluer_geo_datacube_get() {
    local options=$1
    local what=$(bluer_ai_option_choice "$options" catalog,raw,template void)

    local datacube_id=$(bluer_ai_clarify_object $2 .)

    python3 -m bluer_geo.datacube \
        get \
        --what "$what" \
        --datacube_id $datacube_id \
        "${@:3}"
}
