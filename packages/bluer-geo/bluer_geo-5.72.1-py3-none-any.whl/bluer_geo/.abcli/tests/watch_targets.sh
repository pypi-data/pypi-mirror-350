#! /usr/bin/env bash

function test_bluer_geo_watch_targets_cat() {
    bluer_objects_download - $BLUE_GEO_WATCH_TARGET_LIST

    bluer_geo_watch_targets cat \
        Miduk
}

function test_bluer_geo_watch_targets_download() {
    bluer_geo_watch_targets_download
}

function test_bluer_geo_watch_targets_test() {
    bluer_objects_download - $BLUE_GEO_WATCH_TARGET_LIST

    bluer_geo_watch_targets test
}
