#! /usr/bin/env bash

function bluer_geo_action_git_before_push() {
    bluer_geo build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(bluer_ai_git get_branch)" != "main" ]] &&
        return 0

    bluer_geo_watch_targets_upload
    [[ $? -ne 0 ]] && return 1

    cp -v $ABCLI_OBJECT_ROOT/$BLUE_GEO_WATCH_TARGET_LIST/target/shape.geojson \
        $abcli_path_git/bluer-geo/bluer_geo/watch/targets.geojson
    [[ $? -ne 0 ]] && return 1

    bluer_geo pypi build
}
