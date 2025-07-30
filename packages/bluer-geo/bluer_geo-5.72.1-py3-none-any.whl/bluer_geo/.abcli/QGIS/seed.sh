#! /usr/bin/env bash

# internal function to bluer_ai_seed.
function bluer_ai_seed_QGIS() {
    # seed is NOT local
    seed=$(python3 -m bluer_geo.QGIS generate_seed)
}

function bluer_geo_QGIS_seed() {
    bluer_ai_seed QGIS "$@"
}
