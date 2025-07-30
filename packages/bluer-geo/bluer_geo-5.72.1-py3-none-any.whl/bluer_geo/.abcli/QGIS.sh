#! /usr/bin/env bash

export BLUE_GEO_QGIS_PATH_PROFILE="$HOME/Library/Application Support/QGIS/QGIS3/profiles/default"
export BLUE_GEO_QGIS_PATH_EXPRESSIONS=$BLUE_GEO_QGIS_PATH_PROFILE/python/expressions
export BLUE_GEO_QGIS_PATH_EXPRESSIONS_GIT=$abcli_path_git/bluer-geo/bluer_geo/QGIS/expressions
export BLUE_GEO_QGIS_PATH_SHARED=$HOME/Downloads/QGIS
export BLUE_GEO_QGIS_PATH_SERVER=$BLUE_GEO_QGIS_PATH_SHARED/server
export BLUE_GEO_QGIS_PATH_TEMPLATES=$BLUE_GEO_QGIS_PATH_PROFILE/project_templates

export BLUE_GEO_QGIS_TEMPLATES_OBJECT_NAME=QGIS-templates-v1

mkdir -p $BLUE_GEO_QGIS_PATH_SERVER

function bluer_geo_QGIS() {
    local task=$1

    local function_name=bluer_geo_QGIS_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    bluer_ai_log_error "QGIS: $task: command not found."
    return 1
}

bluer_ai_source_caller_suffix_path /QGIS
