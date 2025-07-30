#! /usr/bin/env bash

function test_bluer_geo_seed_QGIS() {
    local options=$1

    bluer_ai_eval ,$options \
        bluer_ai_seed QGIS screen
    [[ $? -ne 0 ]] && return 1

    bluer_ai_eval ,$options \
        bluer_geo_QGIS seed screen
}
