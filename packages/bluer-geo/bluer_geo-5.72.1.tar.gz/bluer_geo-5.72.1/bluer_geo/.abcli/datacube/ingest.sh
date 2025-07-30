#! /usr/bin/env bash

function bluer_geo_datacube_ingest() {
    local options=$1
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local scope=$(bluer_ai_option "$options" scope metadata)
    local do_overwrite=$(bluer_ai_option_int "$options" overwrite 0)
    local do_upload=$(bluer_ai_option_int "$options" upload 0)

    local datacube_id=$(bluer_ai_clarify_object $2 .)

    bluer_ai_log "🧊 ingesting $datacube_id ..."

    local template_object_name=$(bluer_geo_datacube get template $datacube_id)
    local do_copy_template=1
    [[ "$template_object_name" == "unknown-template" ]] &&
        do_copy_template=0
    do_copy_template=$(bluer_ai_option_int "$options" copy_template $do_copy_template)

    [[ "$do_copy_template" == 1 ]] &&
        bluer_objects_clone \
            - \
            $template_object_name \
            $datacube_id

    bluer_ai_eval - \
        python3 -m bluer_geo.datacube \
        ingest \
        --datacube_id $datacube_id \
        --dryrun $do_dryrun \
        --overwrite $do_overwrite \
        --scope $scope \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $datacube_id

    return $status
}
