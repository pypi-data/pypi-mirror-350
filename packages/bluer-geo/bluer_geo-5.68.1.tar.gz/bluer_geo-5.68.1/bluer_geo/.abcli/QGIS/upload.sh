function bluer_geo_QGIS_upload() {
    local object_name=$(bluer_ai_clarify_object $1 .)

    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    local qgz_filename=$object_path/$object_name.qgz
    if [[ -f "$qgz_filename" ]]; then
        local list_of_dependencies=$(python3 -m bluer_geo.QGIS \
            list_dependencies \
            --filename "$qgz_filename" \
            --delim +)
        bluer_ai_log_list "$list_of_dependencies" \
            --before "uploading" \
            --after "dependenci(es)" \
            --delim +

        local dependency_name
        for dependency_name in $(echo $list_of_dependencies | tr + " "); do
            [[ "$dependency_name" == "$object_name" ]] && continue
            bluer_objects_upload - $dependency_name
        done
    fi

    bluer_objects_upload - $object_name
}
