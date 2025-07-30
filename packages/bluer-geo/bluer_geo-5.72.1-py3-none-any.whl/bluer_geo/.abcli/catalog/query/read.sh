#! /usr/bin/env bash

function bluer_geo_catalog_query_read() {
    local options=$1
    local show_len=$(bluer_ai_option_int "$options" len 0)
    local do_all=$(bluer_ai_option_int "$options" all 0)

    local object_name=$(bluer_ai_clarify_object $2 .)

    local extra_args=""
    [[ "$do_all" == 1 ]] &&
        extra_args="--count -1"

    python3 -m bluer_geo.catalog.query \
        read \
        --object_name $object_name \
        --show_len $show_len \
        $extra_args \
        "${@:3}"
}
