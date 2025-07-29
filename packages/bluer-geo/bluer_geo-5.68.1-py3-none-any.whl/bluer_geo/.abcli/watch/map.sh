#! /usr/bin/env bash

function bluer_geo_watch_map() {
    local options=$1

    local algo=$(bluer_ai_option "$options" algo modality)
    local allow_failure=$(bluer_ai_option_int "$options" allow_failure 0)
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_download=$(bluer_ai_option_int "$options" download $(bluer_ai_not $do_dryrun))

    local query_object_name=$(bluer_ai_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        bluer_objects_download - $query_object_name

    bluer_ai_log "🌐 @geo watch map $query_object_name: $options -> @algo"

    bluer_ai_eval - \
        bluer_geo_watch_algo_${algo}_map "$@"
    local status="$?"

    if [[ "$status" -ne 0 ]]; then
        [[ "$allow_failure" == 1 ]] && return $status

        bluer_ai_log_warning "status: $status, ignored."
    fi

    return 0
}
