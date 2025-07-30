#! /usr/bin/env bash

function test_bluer_geo_datacube_crop() {
    local options=$1

    bluer_ai_log_warning "disabled, tracked in https://github.com/kamangir/bluer-geo/issues/2".
    return 0

    local datacube_id=$BLUE_GEO_TEST_DATACUBE_COPERNICUS_SENTINEL_2_CHILCOTIN
    bluer_geo_datacube_ingest \
        scope=rgbx,$options \
        $datacube_id
    [[ $? -ne 0 ]] && return 1

    local suffix=test_bluer_geo_datacube_crop-$(bluer_ai_string_timestamp_short)

    bluer_geo_datacube_crop \
        suffix=$suffix,$options \
        $BLUE_GEO_TEST_DATACUBE_CROP_CTULINE \
        $datacube_id
}
