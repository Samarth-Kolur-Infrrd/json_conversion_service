from converter_utils.value_resolve import resolve_value

def build_group_fields(group, mapping_lookup):
    group_fields = []
    shared_object_id = group[0].get("objectId") if group else None
    for subfield in group:
        m = mapping_lookup.get(subfield["fieldName"])
        if not m:
            continue 
        group_fields.append({
        "field_name": m["customFormatFieldName"],
        "field_value": resolve_value(subfield),
        "field_type": subfield["fieldType"],
        "field_data_type": subfield["dataType"].capitalize(),
        "titan_field_name": subfield["fieldName"],
        "titan_field_id": subfield.get("fieldId"),
        "titan_object_id": subfield.get("objectId", shared_object_id),
        })
    return group_fields