#! /usr/bin/env bash

function bluer_geo_datacube_label() {
    local options=$1
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_download=$(bluer_ai_option_int "$options" download $(bluer_ai_not $do_dryrun))
    local do_open_QGIS=$(bluer_ai_option_int "$options" QGIS 1)
    local do_rasterize=$(bluer_ai_option_int "$options" rasterize 1)
    local do_sync=$(bluer_ai_option_int "$options" sync 1)
    local do_upload=$(bluer_ai_option_int "$options" upload 0)

    local datacube_id=$(bluer_ai_clarify_object $2 .)

    bluer_objects_mlflow_tags_set \
        $datacube_id \
        labelled

    if [[ "$do_sync" == 1 ]]; then
        if [[ "$do_download" == 1 ]]; then
            local template_path=$ABCLI_OBJECT_ROOT/$datacube_id/template
            mkdir -pv $template_path

            aws s3 sync \
                "$ABCLI_S3_OBJECT_PREFIX/$datacube_id/template" \
                "$template_path" \
                --exact-timestamps
            [[ $? -ne 0 ]] && return 1
        fi

        bluer_ai_eval dryrun=$do_dryrun \
            python3 -m bluer_geo.datacube.label \
            sync \
            --datacube_id $datacube_id
        [[ $? -ne 0 ]] && return 1
    fi

    if [[ "$do_open_QGIS" == 1 ]]; then
        bluer_ai_open QGIS $datacube_id

        bluer_ai_wait "ready to save the labels?"
        [[ $? -ne 0 ]] && return 1
    fi

    if [[ "$do_rasterize" == 1 ]]; then
        bluer_ai_eval dryrun=$do_dryrun \
            python3 -m bluer_geo.datacube.label \
            rasterize \
            --datacube_id $datacube_id
        [[ $? -ne 0 ]] && return 1
    fi

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $datacube_id

    return 0
}
