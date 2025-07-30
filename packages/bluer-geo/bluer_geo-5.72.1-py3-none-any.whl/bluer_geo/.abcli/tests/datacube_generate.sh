#! /usr/bin/env bash

function test_bluer_geo_datacube_generate() {
    local options=$1
    local list_of_product=$(bluer_ai_option "$options" product FRE+SRE)

    # TODO: remove after the SkyFox fix.
    return 0

    local datacube_id=$BLUE_GEO_TEST_DATACUBE_SKYFOX_VENUS

    local product
    for product in $(echo $list_of_product | tr + " "); do
        bluer_ai_log "product: $product"

        bluer_geo_datacube_ingest \
            scope=rgbx+_${product}_,$options \
            $datacube_id
        [[ $? -ne 0 ]] && return 1

        bluer_geo_datacube_generate \
            ,$options \
            $datacube_id \
            --modality rgb@$product
        [[ $? -ne 0 ]] && return 1

        bluer_ai_hr
    done
}
