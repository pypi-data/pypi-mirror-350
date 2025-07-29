#! /usr/bin/env bash

function bluer_geo_watch_targets_cat() {
    local target_name=$1
    if [[ -z "$target_name" ]]; then
        bluer_ai_log_error "@targets cat: <target-name> not found."
        return 1
    fi

    python3 -m bluer_geo.watch.targets \
        get \
        --target_name $target_name \
        --what one_liner \
        "${@:2}"
}
