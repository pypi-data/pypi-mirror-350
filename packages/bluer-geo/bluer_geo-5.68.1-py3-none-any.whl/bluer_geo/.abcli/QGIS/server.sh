#! /usr/bin/env bash

function bluer_geo_QGIS_server() {
    local prompt="🌐 $(bluer_geo version).QGIS server ... (^C to stop)"
    bluer_ai_log $prompt

    bluer_ai_badge "🌐"

    local filename
    cd $BLUE_GEO_QGIS_PATH_SERVER
    while true; do
        sleep 1
        for filename in *.command; do
            if [ -e "$filename" ]; then
                local command=$(cat $filename)
                bluer_ai_log "$filename: $command"

                bluer_ai_eval - "$command"
                rm -v $filename

                bluer_ai_log $prompt
            fi
        done
    done
}
