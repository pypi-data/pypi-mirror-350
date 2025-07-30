#! /usr/bin/env bash

function bluer_geo_watch_algo_modality_map() {
    local options=$1
    local algo=$(bluer_ai_option "$options" algo modality)
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local modality=$(bluer_ai_option "$options" modality rgb)
    local offset=$(bluer_ai_option "$options" offset 0)
    local suffix=$(bluer_ai_option "$options" suffix $(bluer_ai_string_timestamp_short))
    local do_upload=$(bluer_ai_option_int "$options" upload $(bluer_ai_not $do_dryrun))

    local query_object_name=$2

    local datacube_id=$(bluer_geo_catalog_query_read - \
        $query_object_name \
        --count 1 \
        --offset $offset)
    if [[ -z "$datacube_id" ]]; then
        bluer_ai_log_warning "offset=$offset: datacube-id not found."
        return 0
    fi

    bluer_ai_log "🌐 @geo watch $algo map $query_object_name @ $offset==$datacube_id -> /$suffix"

    local product=$(python3 -c "print('$modality'.split('@',1)[1] if '@' in '$modality' else '')")
    [[ ! -z "$product" ]] &&
        bluer_ai_log "product: $product"

    if [[ "$datacube_id" == *"DERIVED"* ]]; then
        bluer_objects_download - \
            $datacube_id
    else
        local scope="rgbx"
        [[ ! -z "$product" ]] && scope=$scope+_${product}_

        bluer_geo_datacube_ingest \
            dryrun=$do_dryrun,scope=$scope \
            $datacube_id
    fi

    local object_name=$query_object_name-$suffix-$offset

    bluer_geo_watch_targets copy - \
        $query_object_name \
        $object_name

    local crop_suffix=$(bluer_ai_string_timestamp_short)
    bluer_geo_datacube_crop \
        dryrun=$do_dryrun,suffix=$crop_suffix \
        $object_name \
        $datacube_id
    [[ $? -ne 0 ]] && return 1

    local cropped_datacube_id=$datacube_id-DERIVED-crop-$crop_suffix

    bluer_geo_datacube_generate \
        dryrun=$do_dryrun \
        $cropped_datacube_id \
        --modality $modality
    [[ $? -ne 0 ]] && return 1

    local scope="rgb"
    [[ ! -z "$product" ]] && scope=$scope+_${product}_
    local filename=$(bluer_geo_datacube_list $cropped_datacube_id \
        --scope $scope \
        --log 0 \
        --count 1 \
        --exists 1)
    if [[ -z "$filename" ]]; then
        bluer_ai_log_warning "offset=$offset: $cropped_datacube_id: file not found."

        [[ "$do_upload" == 1 ]] &&
            bluer_objects_upload - $object_name

        return 0
    fi
    cp -v \
        $ABCLI_OBJECT_ROOT/$cropped_datacube_id/$filename \
        $ABCLI_OBJECT_ROOT/$object_name/

    bluer_ai_eval dryrun=$do_dryrun \
        python3 -m bluer_geo.watch.algo.$algo \
        map \
        --query_object_name $query_object_name \
        --suffix $suffix \
        --offset $offset \
        --modality $modality \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    return $status
}
