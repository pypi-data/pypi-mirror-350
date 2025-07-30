#! /usr/bin/env bash

function bluer_geo_datacube_crop() {
    local options=$1
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_download=$(bluer_ai_option_int "$options" download $(bluer_ai_not $do_dryrun))
    local suffix=$(bluer_ai_option "$options" suffix $(bluer_ai_string_timestamp_short))

    local object_name=$(bluer_ai_clarify_object $2 ..)
    [[ "$do_download" == 1 ]] &&
        bluer_objects_download - $object_name

    local cutline=$ABCLI_OBJECT_ROOT/$object_name/target/shape.geojson
    if [[ ! -f "$cutline" ]]; then
        bluer_ai_log_error "@datacube: crop: $cutline: file not found."
        return 1
    fi

    local datacube_id=$(bluer_ai_clarify_object $3 .)

    local cropped_datacube_id=$datacube_id-DERIVED-crop-$suffix

    bluer_geo_watch_targets copy - \
        $object_name \
        $cropped_datacube_id

    local crs=$(bluer_geo_gdal_get_crs $cutline)
    bluer_ai_log "cutline crs: $crs"

    local list_of_files=$(bluer_geo_datacube_list $datacube_id \
        --delim space \
        --exists 1 \
        --scope raster \
        --log 0)
    local filename
    local source_filename
    local destination_filename
    for filename in $list_of_files; do
        source_filename=$ABCLI_OBJECT_ROOT/$datacube_id/$filename

        local source_filename_crs=$(bluer_geo_gdal_get_crs $source_filename)
        bluer_ai_log "cropping $filename @ $source_filename_crs ..."

        destination_filename=$ABCLI_OBJECT_ROOT/$cropped_datacube_id/$filename
        destination_path=$(dirname "$destination_filename")
        mkdir -pv $destination_path

        bluer_ai_eval dryrun=$do_dryrun \
            gdalwarp -cutline $cutline \
            -crop_to_cutline \
            -dstalpha \
            -t_srs $crs \
            $source_filename \
            $destination_filename

        local destination_filename_crs=$(bluer_geo_gdal_get_crs $destination_filename)
        bluer_ai_log "output crs: $destination_filename_crs - expected $crs."
    done

    return 0
}
