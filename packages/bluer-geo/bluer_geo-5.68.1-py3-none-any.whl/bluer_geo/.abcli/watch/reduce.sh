#! /usr/bin/env bash

function bluer_geo_watch_reduce() {
    local options=$1
    local algo=$(bluer_ai_option "$options" algo modality)
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_download=$(bluer_ai_option_int "$options" download $(bluer_ai_not $do_dryrun))
    local do_upload=$(bluer_ai_option_int "$options" upload $(bluer_ai_not $do_dryrun))
    local suffix=$(bluer_ai_option "$options" suffix)
    if [[ -z "$suffix" ]]; then
        bluer_ai_log_error "@geo: watch: reduce: suffix not found."
        return 1
    fi

    local query_object_name=$(bluer_ai_clarify_object $2 ..)
    [[ "$do_download" == 1 ]] &&
        bluer_objects_download - $query_object_name

    local object_name=$(bluer_ai_clarify_object $3 .)
    [[ "$do_download" == 1 ]] &&
        bluer_objects_download - $object_name

    bluer_geo_watch_targets copy - \
        $query_object_name \
        $object_name

    bluer_ai_log "🌐 @geo watch reduce $query_object_name/$suffix -> $object_name"

    local datacube_id_list=$(bluer_objects_metadata get \
        delim=space,key=datacube_id,object \
        $query_object_name)
    bluer_ai_log_list "$datacube_id_list" \
        --before "reducing" \
        --delim space \
        --after "datacube(s)"

    local datacube_id
    local offset=0
    local leaf_object_name
    for datacube_id in $datacube_id_list; do
        leaf_object_name=$query_object_name-$suffix-$(python3 -c "print(f'{$offset:03d}')")
        bluer_ai_log "reducing $leaf_object_name ..."

        bluer_objects_clone \
            cp,~relate,~tags \
            $leaf_object_name \
            $object_name

        offset=$((offset + 1))
    done

    bluer_ai_eval - \
        bluer_geo_watch_algo_${algo}_reduce "$@"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    return $status
}
