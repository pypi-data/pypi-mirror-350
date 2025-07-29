#! /usr/bin/env bash

function bluer_geo_catalog_list() {
    local options=$1
    local what=$(bluer_ai_option_choice "$options" catalogs,collections,datacubes,datacube_classes catalogs)

    python3 -m bluer_geo.catalog \
        list \
        --what "$what" \
        "${@:2}"
}

function bluer_geo_catalog_ls() {
    bluer_geo_catalog_list "$@"
}

function bluer_geo_catalog_load_all() {
    bluer_ai_log_list $bluer_geo_list_of_catalogs \
        --delim , \
        --before "🌐 loading" \
        --after "catalog(s)"

    local catalog
    local list_of_collections
    for catalog in $(echo $bluer_geo_list_of_catalogs | tr , " "); do
        bluer_ai_source_caller_suffix_path /$catalog ignore_error

        list_of_datacube_classes=$(bluer_geo_catalog list \
            datacube_classes \
            --catalog $catalog \
            --log 0)
        bluer_ai_log_list "$list_of_datacube_classes" \
            --before "🧊 $GREEN$catalog$NC: loaded" \
            --after "collection(s)"
    done

    return 0
}

export bluer_geo_list_of_catalogs=$(bluer_geo_catalog_list catalogs --log 0)

bluer_geo_catalog_load_all
