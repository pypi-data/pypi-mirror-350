#! /usr/bin/env bash

function bluer_geo_watch_targets_update_template() {
    local options=$1
    local target_name=$(bluer_ai_option "$options" target Miduk)
    local do_download=$(bluer_ai_option "$options" download 1)
    local do_upload=$(bluer_ai_option "$options" upload 1)

    [[ "$do_download" == 1 ]] &&
        bluer_objects_download - $BLUE_GEO_QGIS_TEMPLATE_WATCH

    local object_name=$(bluer_ai_clarify_object $2 .)

    python3 -m bluer_geo.watch.targets save \
        --target_name $target_name \
        --object_name $BLUE_GEO_QGIS_TEMPLATE_WATCH \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $BLUE_GEO_QGIS_TEMPLATE_WATCH

    return $status
}
