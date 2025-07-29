#! /usr/bin/env bash

function test_bluer_geo_logging() {
    local options=$1

    bluer_ai_log_warning "disabled, tracked in https://github.com/kamangir/bluer-geo/issues/2".
    return 0

    bluer_geo log \
        filename=1050010040277300-visual.tif,$options \
        $BLUE_GEO_TEST_DATACUBE_MAXAR_OPEN_DATA
}
