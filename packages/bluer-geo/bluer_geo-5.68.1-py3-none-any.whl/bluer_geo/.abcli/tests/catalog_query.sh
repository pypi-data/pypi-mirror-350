#! /usr/bin/env bash

function test_bluer_geo_catalog_query() {
    local options=$1
    local list_of_catalogs=$(echo $bluer_geo_list_of_catalogs | tr , +)
    list_of_catalogs=$(bluer_ai_option "$options" catalog $list_of_catalogs)

    bluer_ai_log_warning "disabled, tracked in https://github.com/kamangir/bluer-geo/issues/2".
    return 0

    bluer_geo_watch_targets_download

    local catalog
    local datacube_class
    for catalog in $(echo $list_of_catalogs | tr + " "); do
        [[ "$catalog" == generic ]] && continue

        local list_of_datacube_classes=$(bluer_geo_catalog list \
            datacube_classes \
            --catalog $catalog \
            --delim , \
            --log 0)
        [[ $? -ne 0 ]] && return 1

        for datacube_class in $(echo $list_of_datacube_classes | tr , " "); do
            bluer_ai_log "testing $catalog/$datacube_class/query ..."

            local object_name="bashtest-$catalog-$datacube_class-$(bluer_ai_string_timestamp)"

            local target=$(bluer_geo_watch_targets list \
                --catalog_name $catalog \
                --collection $datacube_class \
                --count 1 \
                --log 0)

            local query_args=""
            if [[ ! -z "$target" ]]; then
                bluer_ai_log "🎯 target: $target"
                query_args=$(bluer_geo_watch_targets get \
                    --what query_args \
                    --target_name $target \
                    --delim space \
                    --log 0)
            fi

            bluer_ai_eval ,$options \
                bluer_geo catalog query $catalog $datacube_class \
                ingest \
                $object_name $query_args
            [[ $? -ne 0 ]] && return 1

            bluer_ai_assert \
                $(bluer_geo catalog query read len $object_name) \
                0 \
                not
            [[ $? -ne 0 ]] && return 1

            local datacube_id=$(bluer_geo catalog query read - $object_name)

            local public_name=datacube-$catalog-$datacube_class

            bluer_ai_hr
        done
    done
    return 0
}
