#! /usr/bin/env bash

function test_bluer_geo_README() {
    local options=$1

    bluer_ai_eval ,$options \
        bluer_geo build_README
}
