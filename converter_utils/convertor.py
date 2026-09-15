import logging

from converter_utils.value_resolve import resolve_value
from converter_utils.build_metadata import build_metadata
from converter_utils.build_common_fields import build_common_fields
from converter_utils.build_group_fields import build_group_fields
from converter_utils.get_mapping import build_mapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform(document, business_type, documentType, listDocument, request_id, request_status):
    object_list_field = next((f for f in document["fields"] if f["type"] == "Object List"), None)
    groups = object_list_field["values"] if object_list_field else [[]] 
    mapping_lookup = build_mapping(business_type)

    common_fields = build_common_fields(document, object_list_field, mapping_lookup)

    output_documents = []   
    for group_index, group in enumerate(groups):
        group_fields = build_group_fields(group, mapping_lookup)

        output_documents.append({
        **build_metadata(
            document,
            business_type,
            documentType,
            listDocument,
            request_id,
            request_status,
            
        ),
        "fields": common_fields + group_fields,
        })

    return output_documents