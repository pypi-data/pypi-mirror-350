#! /usr/bin/env bash

function bluer_geo_watch() {
    local options=$1
    local target_options=$2
    local algo_options=$3
    local workflow_options=$4
    local map_options=$5
    local reduce_options=$6

    bluer_geo_watch_targets_download

    local task
    for task in map reduce targets query; do
        if [ $(bluer_ai_option_int "$options" $task 0) == 1 ]; then
            bluer_geo_watch_$task "${@:2}"
            return
        fi
    done

    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)

    local algo=$(bluer_ai_option "$algo_options" algo modality)

    local object_name=$(bluer_ai_clarify_object $7 geo-watch-$(bluer_ai_string_timestamp))

    local target=$(bluer_ai_option "$target_options" target)
    local query_object_name
    if [[ -z "$target" ]]; then
        query_object_name=$target_options

        bluer_ai_download - $query_object_name
    else
        query_object_name=$object_name-query-$(bluer_ai_string_timestamp_short)

        bluer_geo_watch_query \
            $target_options \
            $query_object_name
        [[ $? -ne 0 ]] && return 1
    fi

    local job_name="$object_name-job-$(bluer_ai_string_timestamp_short)"

    bluer_objects_mlflow_tags_set $object_name job=$job_name

    bluer_ai_log "🌐 @geo: watch: $query_object_name: -[ $workflow_options @ $map_options + $reduce_options @ $job_name]-> $object_name"

    bluer_objects_clone \
        upload \
        $BLUE_GEO_QGIS_TEMPLATE_WATCH \
        $object_name

    bluer_ai_eval dryrun=$do_dryrun \
        python3 -m bluer_geo.watch.workflow \
        generate \
        --algo_options $algo_options \
        --query_object_name $query_object_name \
        --job_name $job_name \
        --object_name $object_name \
        --map_options ",$map_options" \
        --reduce_options ",$reduce_options" \
        "${@:8}"
    [[ $? -ne 0 ]] && return 1

    bluer_ai_eval - \
        bluer_geo_watch_algo_${algo}_generate "$@"
    [[ $? -ne 0 ]] && return 1

    local do_submit=$(bluer_ai_option_int "$workflow_options" submit 1)
    [[ "$do_submit" == 0 ]] && return 0

    bluer_ai_eval dryrun=$do_dryrun \
        bluer_flow_workflow_submit \
        ~download,$workflow_options \
        $job_name
}

bluer_ai_source_caller_suffix_path /watch

bluer_ai_source_caller_suffix_path /watch/algo/diff
bluer_ai_source_caller_suffix_path /watch/algo/modality
