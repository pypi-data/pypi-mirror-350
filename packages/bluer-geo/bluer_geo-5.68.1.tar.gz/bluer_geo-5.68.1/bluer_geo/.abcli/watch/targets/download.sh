#! /usr/bin/env bash

function bluer_geo_watch_targets_download() {
    local options=$1

    bluer_objects_download - \
        $BLUE_GEO_WATCH_TARGET_LIST \
        "$@"

    bluer_ai_list_log "$(python3 -m bluer_geo.watch.targets \
        list \
        --log 0)" \
        --before "downloaded" \
        --after "target(s)"
}
