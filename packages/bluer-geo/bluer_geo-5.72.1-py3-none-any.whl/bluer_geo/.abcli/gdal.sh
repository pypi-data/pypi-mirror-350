#! /usr/bin/env bash

function bluer_geo_gdal() {
    local task=$1

    local function_name=bluer_geo_gdal_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    bluer_ai_log_error "@gdal: $task: command not found."
    return 1
}

bluer_ai_source_caller_suffix_path /gdal
