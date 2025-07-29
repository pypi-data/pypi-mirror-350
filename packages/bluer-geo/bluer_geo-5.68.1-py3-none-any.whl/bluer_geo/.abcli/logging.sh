#! /usr/bin/env bash

function bluer_geo_log() {
    local options=$1
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_download=$(bluer_ai_option_int "$options" download $(bluer_ai_not $do_dryrun))
    local do_upload=$(bluer_ai_option_int "$options" upload 0)
    local filename=$(bluer_ai_option "$options" filename void)

    local object_name=$(bluer_ai_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        bluer_objects_download - $object_name

    bluer_ai_eval do_dryrun=$do_dryrun \
        python3 -m bluer_geo.logger log_geoimage \
        --object_name $object_name \
        --filename $filename \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    return $status
}
