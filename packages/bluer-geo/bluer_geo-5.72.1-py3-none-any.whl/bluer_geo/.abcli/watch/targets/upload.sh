#! /usr/bin/env bash

function bluer_geo_watch_targets_upload() {
    python3 -m bluer_geo.watch.targets test
    [[ $? -ne 0 ]] && return 1

    bluer_geo_watch_targets \
        save \
        target=all \
        $BLUE_GEO_WATCH_TARGET_LIST
    [[ $? -ne 0 ]] && return 1

    bluer_objects_upload - $BLUE_GEO_WATCH_TARGET_LIST
}
