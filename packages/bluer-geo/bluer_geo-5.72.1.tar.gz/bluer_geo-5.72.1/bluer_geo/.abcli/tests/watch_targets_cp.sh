#! /usr/bin/env bash

function test_bluer_geo_watch_targets_cp() {
    local object_1_name="test_bluer_geo_watch_targets_cp-$(bluer_ai_string_timestamp)"
    local object_2_name="test_bluer_geo_watch_targets_cp-$(bluer_ai_string_timestamp)"

    bluer_geo_watch_targets save \
        target=Miduk \
        $object_1_name
    [[ $? -ne 0 ]] && return 1

    bluer_geo_watch_targets cp - \
        $object_1_name \
        $object_2_name
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert_file_exists \
        $ABCLI_OBJECT_ROOT/$object_2_name/target/shape.geojson
}
