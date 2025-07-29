#! /usr/bin/env bash

function test_bluer_geo_datacube_list() {
    local datacube_id

    for datacube_id in \
        void \
        datacube-generic; do
        bluer_ai_assert \
            "$(bluer_geo_datacube_list $datacube_id --log 0)" \
            - empty
        [[ $? -ne 0 ]] && return 1
    done

    for datacube_id in \
        $BLUE_GEO_TEST_DATACUBE_COPERNICUS_SENTINEL_2 \
        $BLUE_GEO_TEST_DATACUBE_FIRMS_AREA \
        $BLUE_GEO_TEST_DATACUBE_MAXAR_OPEN_DATA \
        $BLUE_GEO_TEST_DATACUBE_UKRAINE_TIMEMAP; do
        bluer_ai_assert \
            $(bluer_geo_datacube_list $datacube_id --log 0) \
            - non-empty
        [[ $? -ne 0 ]] && return 1
    done

    return 0
}
