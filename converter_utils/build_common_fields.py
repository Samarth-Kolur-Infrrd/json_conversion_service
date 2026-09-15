from converter_utils.get_mapping import build_mapping
from converter_utils.value_resolve import resolve_value

def build_common_fields(document, object_list_field, mapping_lookup):
    common_fields = []

    for field in document["fields"]:
        if field is object_list_field:
            continue
        m = mapping_lookup.get(field["name"])
        if not m:
            continue 
        common_fields.append({
            "field_name": m["customFormatFieldName"],
            "field_value": resolve_value(field),
            "field_type": field["type"],
            "field_data_type": field["dataType"].capitalize(),
        })
    return common_fields
