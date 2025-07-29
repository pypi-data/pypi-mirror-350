#! /usr/bin/env bash

function bluer_geo() {
    local task=$1

    if [ "$task" == "pylint" ]; then
        bluer_ai_${task} ignore=bluer_geo/QGIS,plugin=bluer_geo,$2 \
            "${@:3}"
        return
    fi

    bluer_ai_generic_task \
        plugin=bluer_geo,task=$task \
        "${@:2}"
}

bluer_ai_log $(bluer_geo version --show_icon 1)

gdalinfo --version
