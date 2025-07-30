#! /usr/bin/env bash

function test_bluer_geo_watch_targets_save() {
    bluer_objects_download - $BLUE_GEO_WATCH_TARGET_LIST

    local target_name
    for target_name in Miduk all; do
        local object_name="test_bluer_geo_watch_targets_save-$target_name-$(bluer_ai_string_timestamp)"

        bluer_geo_watch_targets save \
            target=$target_name \
            $object_name

        bluer_ai_assert_file_exists \
            $ABCLI_OBJECT_ROOT/$object_name/target/shape.geojson
        [[ $? -ne 0 ]] && return 1

        bluer_ai_hr
    done

    return 0
}
