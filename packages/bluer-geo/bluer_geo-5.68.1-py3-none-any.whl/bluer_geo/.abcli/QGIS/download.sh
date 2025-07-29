function bluer_geo_QGIS_download() {
    local object_name=$(bluer_ai_clarify_object $1 .)

    bluer_objects_download filename=$object_name.qgz $object_name
    [[ $? -ne 0 ]] && return 1

    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    local qgz_filename=$object_path/$object_name.qgz

    local list_of_dependencies=$(python3 -m bluer_geo.QGIS \
        list_dependencies \
        --filename "$qgz_filename" \
        --delim +)
    bluer_ai_log_list "$list_of_dependencies" \
        --before "downloading" \
        --after "dependenci(es)" \
        --delim +

    local dependency_name
    for dependency_name in $(echo $list_of_dependencies | tr + " "); do
        [[ "$dependency_name" == "$object_name" ]] && continue
        bluer_objects_download - $dependency_name
    done

    bluer_objects_download - $object_name \
        QGIS,"${@:2}"
}
