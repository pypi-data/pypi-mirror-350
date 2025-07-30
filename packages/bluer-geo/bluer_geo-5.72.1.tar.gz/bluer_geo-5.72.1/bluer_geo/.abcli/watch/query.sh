#! /usr/bin/env bash

function bluer_geo_watch_query() {
    local options=$1
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_upload=$(bluer_ai_option_int "$options" upload $(bluer_ai_not $do_dryrun))

    local target=$(bluer_ai_option "$options" target)
    if [[ -z "$target" ]]; then
        bluer_ai_log_error "target not found."
        return 1
    fi

    local target_exists=$(bluer_geo_watch_targets get \
        --what exists \
        --target_name $target \
        --log 0)
    if [[ "$target_exists" != 1 ]]; then
        bluer_ai_log_error "$target: target not found."
        return 1
    fi

    local catalog=$(bluer_geo_watch_targets get \
        --what catalog \
        --target_name $target \
        --log 0)
    local collection=$(bluer_geo_watch_targets get \
        --what collection \
        --target_name $target \
        --log 0)
    local query_args=$(bluer_geo_watch_targets get \
        --what query_args \
        --target_name $target \
        --delim space \
        --log 0)

    local object_name=$(bluer_ai_clarify_object $2 .)

    bluer_ai_log "🎯 $target: $catalog/$collection: $query_args -> $object_name"

    bluer_ai_eval dryrun=$do_dryrun \
        bluer_geo_catalog_query $catalog \
        $collection \
        - \
        $object_name \
        --count -1 \
        $query_args
    [[ $? -ne 0 ]] && return 1

    bluer_geo_watch_targets_save \
        target=$target \
        $object_name
    [[ $? -ne 0 ]] && return 1

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    return 0
}
