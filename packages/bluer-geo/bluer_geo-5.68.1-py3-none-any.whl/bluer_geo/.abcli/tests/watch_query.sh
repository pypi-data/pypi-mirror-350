#! /usr/bin/env bash

function test_bluer_geo_watch_query() {
    local options=$1

    bluer_ai_log_warning "disabled, tracked in https://github.com/kamangir/bluer-geo/issues/2".
    return 0

    local list_of_targets=$(bluer_ai_option "$options" target Miduk)

    local target
    for target in $(echo $list_of_targets | tr + " "); do
        local object_name=test_bluer_geo_watch_query-$target-$(bluer_ai_string_timestamp)

        bluer_geo_watch_query \
            target=$target \
            $object_name
        [[ $? -ne 0 ]] && return 1

        bluer_ai_hr
    done

    return 0
}
