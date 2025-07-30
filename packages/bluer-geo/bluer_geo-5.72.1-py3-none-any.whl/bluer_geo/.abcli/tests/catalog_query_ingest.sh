#! /usr/bin/env bash

function test_bluer_geo_catalog_query_ingest() {
    local options=$1

    bluer_ai_eval ,$options \
        bluer_geo_catalog_query_ingest \
        download \
        $BLUE_GEO_TEST_QUERY_OBJECT_PALISADES_MAXAR_TEST \
        scope=rgb
}
