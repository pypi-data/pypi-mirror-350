#! /usr/bin/env bash

function bluer_geo_QGIS_expressions() {
    local task=$1

    if [[ "$task" == pull ]]; then
        rsync \
            -avv \
            "$BLUE_GEO_QGIS_PATH_EXPRESSIONS_GIT/" \
            "$BLUE_GEO_QGIS_PATH_EXPRESSIONS/"
        return
    fi

    if [[ "$task" == push ]]; then
        local options=$2
        local do_push=$(bluer_ai_option_int "$options" push 0)

        rsync \
            -avv \
            --exclude='__pycache__' \
            --exclude='default.py' \
            --exclude='__init__.py' \
            "$BLUE_GEO_QGIS_PATH_EXPRESSIONS/" \
            "$BLUE_GEO_QGIS_PATH_EXPRESSIONS_GIT/"

        return
    fi

    bluer_ai_log_error "QGIS: expressions: $task: command not found."
    return 1
}
