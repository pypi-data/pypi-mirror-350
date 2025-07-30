#! /usr/bin/env bash

function test_bluer_geo_datacube_label() {
    local datacube_id=$BLUE_GEO_PALISADES_TEST_DATACUBE

    bluer_ai_log_warning "disabled, tracked in https://github.com/kamangir/bluer-geo/issues/2".
    return 0

    bluer_geo_datacube_ingest \
        scope=rgb \
        $datacube_id

    bluer_geo_datacube_label ~QGIS \
        $datacube_id
}
