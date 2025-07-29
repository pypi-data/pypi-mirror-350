#! /usr/bin/env bash

function test_bluer_geo_version() {
    local options=$1

    bluer_ai_eval ,$options \
        "bluer_geo version ${@:2}"

    return 0
}
