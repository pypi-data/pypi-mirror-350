#! /usr/bin/env bash

function test_bluer_geo_watch_targets_list() {
    bluer_objects_download - $BLUE_GEO_WATCH_TARGET_LIST

    bluer_ai_assert \
        $(bluer_geo_watch_targets list \
            --delim + \
            --log 0) \
        - non-empty
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_geo_watch_targets list \
            --catalog_name copernicus \
            --collection sentinel_2 \
            --delim + \
            --log 0) \
        - non-empty
}
