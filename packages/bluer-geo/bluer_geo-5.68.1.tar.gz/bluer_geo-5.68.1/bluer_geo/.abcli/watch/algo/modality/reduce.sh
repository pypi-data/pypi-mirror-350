#! /usr/bin/env bash

function bluer_geo_watch_algo_modality_reduce() {
    local options=$1
    local algo=$(bluer_ai_option "$options" algo modality)
    local content_threshold=$(bluer_ai_option "$options" content 0.5)
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local suffix=$(bluer_ai_option "$options" suffix)

    local query_object_name=$(bluer_ai_clarify_object $2 ..)

    local object_name=$(bluer_ai_clarify_object $3 .)

    bluer_ai_log "@geo: watch: algo: $algo: reduce"

    bluer_ai_eval dryrun=$do_dryrun \
        python3 -m bluer_geo.watch.algo.$algo \
        reduce \
        --content_threshold $content_threshold \
        --query_object_name $query_object_name \
        --suffix $suffix \
        --object_name $object_name \
        "${@:4}"
}
