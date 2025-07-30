#! /usr/bin/env bash

function bluer_geo_catalog_browse() {
    local catalog=$1
    if [[ ",$bluer_geo_list_of_catalogs," != *",$catalog,"* ]]; then
        bluer_ai_log_error "@catalog: browse: $catalog: catalog not found."
        return 1
    fi

    local what=$2

    local url=$(bluer_geo_catalog_get \
        "url:$what" \
        --catalog $catalog \
        "${@:3}")

    bluer_ai_browse $url
}
