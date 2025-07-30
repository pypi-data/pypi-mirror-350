#! /usr/bin/env bash

function test_bluer_geo_catalog_browse() {
    local options=$1

    local catalog
    for catalog in $(echo $bluer_geo_list_of_catalogs | tr , " "); do
        bluer_ai_eval ,$options \
            bluer_geo catalog browse $catalog
        [[ $? -ne 0 ]] && return 1
    done

    return 0
}
