#! /usr/bin/env bash

function bluer_geo_watch_algo_diff_map() {
    local options=$1
    local algo=$(bluer_ai_option "$options" algo diff)
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local depth=$(bluer_ai_option "$options" depth 2)
    local offset=$(bluer_ai_option "$options" offset 0)
    local dynamic_range=$(bluer_ai_option "$options" range $BLUE_GEO_WATCH_ALGO_DIFF_MAP_DYNAMIC_RANGE)
    local suffix=$(bluer_ai_option "$options" suffix $(bluer_ai_string_timestamp_short))
    local do_upload=$(bluer_ai_option_int "$options" upload $(bluer_ai_not $do_dryrun))

    local query_object_name=$2

    local offset_int=$(python3 -c "print(int('$offset'))")

    local index
    local index_000
    for ((index = offset_int; index < offset_int + depth; index++)); do
        index_000=$(python3 -c "print(f'{$index:03d}')")
        bluer_geo_watch_algo_modality_map \
            ,$options,algo=modality,offset=$index_000,suffix=$suffix-$offset-D,~upload \
            "${@:2}"
        [[ $? -ne 0 ]] && return 1
    done

    local object_name=$query_object_name-$suffix-$offset

    bluer_geo_watch_targets copy - \
        $query_object_name \
        $object_name

    bluer_ai_eval dryrun=$do_dryrun \
        python3 -m bluer_geo.watch.algo.$algo \
        map \
        --query_object_name $query_object_name \
        --suffix $suffix \
        --offset $offset \
        --depth $depth \
        --dynamic_range $dynamic_range \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    return $status
}
