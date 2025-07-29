#!/bin/bash

function bluer_geo_QGIS_templates() {
    local task=$1

    local object_name=$BLUE_GEO_QGIS_TEMPLATES_OBJECT_NAME
    local object_path=$ABCLI_OBJECT_ROOT/$object_name

    if [ "$task" == "download" ]; then
        bluer_objects_download - $object_name

        rsync \
            -avv \
            $object_path/ \
            "$BLUE_GEO_QGIS_PATH_TEMPLATES/"
        return
    fi

    if [ "$task" == "upload" ]; then
        rsync \
            -avv \
            "$BLUE_GEO_QGIS_PATH_TEMPLATES/" \
            $object_path/

        bluer_objects_upload - $object_name

        return
    fi

    bluer_ai_log_error "@QGIS: templates: $task: command not found."
}
