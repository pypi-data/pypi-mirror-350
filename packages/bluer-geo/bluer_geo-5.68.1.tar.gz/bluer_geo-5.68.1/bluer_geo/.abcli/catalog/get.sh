#! /usr/bin/env bash

function bluer_geo_catalog_get() {
    python3 -m bluer_geo.catalog \
        get \
        --what "$1" \
        "${@:2}"
}
