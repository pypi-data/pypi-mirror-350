#! /usr/bin/env bash

function bluer_geo_watch_targets_publish() {
    local options=$1
    local use_template=$(bluer_ai_option_int "$options" template 0)

    local object_name=$BLUE_GEO_WATCH_TARGET_LIST
    [[ "$use_template" == 1 ]] &&
        object_name=$BLUE_GEO_QGIS_TEMPLATE_WATCH

    bluer_objects_publish \
        tar \
        $object_name
}
