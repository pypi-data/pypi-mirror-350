#! /usr/bin/env bash

function test_bluer_geo_watch() {
    local options=$1

    bluer_ai_log_warning "disabled, tracked in https://github.com/kamangir/bluer-geo/issues/2".
    return 0

    local list_of_targets=$(bluer_ai_option "$options" target Miduk-test)
    local list_of_algo=$(bluer_ai_option "$options" algo modality+diff)

    local algo
    local target
    for algo in $(echo $list_of_algo | tr + " "); do
        for target in $(echo $list_of_targets | tr + " "); do
            bluer_ai_log "🎯 $algo on $target ..."

            local object_name=test_bluer_geo_watch-$algo-$target-$(bluer_ai_string_timestamp)

            bluer_geo_watch \
                ,$options \
                target=$target \
                algo=$algo \
                to=local \
                - \
                - \
                $object_name
            [[ $? -ne 0 ]] && return 1

            bluer_ai_hr
        done
    done

    return 0
}
