#! /usr/bin/env bash

function test_bluer_geo_ingest() {
    local options=$1
    local list_of_objects=$(bluer_ai_option "$options" objects global-power-plant-database)

    bluer_ai_log_warning "disabled, tracked in https://github.com/kamangir/bluer-geo/issues/2".
    return 0

    local object_name
    for object_name in $(echo $list_of_objects | tr + " "); do

        bluer_geo_ingest \
            upload,publish,$options \
            $object_name
        [[ $? -ne 0 ]] && return 1

        bluer_ai_hr
    done

    return 0
}
