from flask import Flask, request, jsonify
import json
 
import logging
from seed import fetch_mapping_config, customFormatTranslatedDocuments

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def resolve_value(field):
    if field.get("dataType", "").lower() == "dropdown":
        value_object = field.get("valueObject", {})

        if "dropdownValue" not in value_object:
            logger.warning(
                "Dropdown field '%s' is missing dropdownValue",
                field.get("name") or field.get("fieldName")
            )
            return ""

        return value_object["dropdownValue"].strip()

    return field.get("value") or field.get("fieldValue") or ""
def build_metadata(
    document,
    business_type,
    document_type,
    listDocument,
    request_id,
    request_status,
):
    return {
        "upload_request_id": request_id,
        "upload_request_status": request_status,
        "document_id": document.get("id"),
        "document_name": document.get("name"),
        "document_file_type": document.get("fileType"),
        "document_processing_status": document.get("status"),
        "file_uploaded_timestamp": document.get("lastModifiedDate"),
        "document_received_timestamp": document.get("documentReceivedDate"),
        "document_extraction_start_timestamp": document.get("documentExtractionStartDate"),
        "business_type": business_type,
        "document_type": document_type.upper(),
        "document_page_count": len(document.get("pages", [])),
        "original_file_page_count": 0,
        "original_file_blank_pages": document.get("totalBlankPages", 0),
        "list_document": listDocument,
        "optional_parameters": document.get("optionalParams", {}),
        "source_document_url": document.get("sourceDocumentUrl")
    }


@app.route("/api/convert", methods=["POST"])
def convert():
    try:
        raw = request.get_data(as_text=True)
        if not raw:
            return jsonify({
                "status": "FAILURE",
                "error": "Request body is missing or invalid JSON"
            }), 400

        if "requestId" not in raw:
            return jsonify({
                "status": "FAILURE",
                "error": "Missing requestId"
            }), 400

        if "status" not in raw:
            return jsonify({
                "status": "FAILURE",
                "error": "Missing status"
            }), 400

        if "documents" not in raw:
            return jsonify({
                "status": "FAILURE",
                "error": "Missing documents"
            }), 400
        
        raw_data = json.loads(raw)
        print("raw:", type(raw_data))
        data = json.loads(raw_data)

        if not isinstance(data["documents"], list):
                    return jsonify({
                        "status": "FAILURE",
                        "error": "documents must be an array"
                    }), 400
                
        with open("requestInput.json","w") as inp:
            json.dump(data,inp,indent=4)

        output = []
        document_ids = []
        transformed_data = []
        for document in data["documents"]:
            businessType = next((m["value"] 
                            for m in document["docTypeHierarchy"] 
                            if m["classificationName"] == "CollateralType"),None)
            if not businessType:
                continue
            documentType =next(m["value"] 
                            for m in document["docTypeHierarchy"] 
                            if m["classificationName"] == "DocumentType")
            listDocument = any(m["classificationName"] == "LIST_TYPE" and (m["value"] == "LIST" or m["value"] == "LIIST")
                                for m in document["docTypeHierarchy"]
                                )
            transformed_data = transform(document, 
                                        businessType,
                                        documentType,
                                        listDocument,
                                        data["requestId"], 
                                        data["status"])
            print(transformed_data)
            output.append(transformed_data)
    
        for documents in transformed_data:
            document_ids.append(documents["document_id"])
        customFormatTranslatedDocuments(output)
        return jsonify({
            "status": "SUCCESS",
            "upload_request_id": data["requestId"],
            "documents_converted": len(output),
            "document_ids": document_ids
        }), 200

    except ValueError as e:

        logger.error("Conversion failed: %s", str(e))

        return jsonify({
            "status": "FAILURE",
            "error": str(e)
        }), 500

    except Exception as e:

        logger.exception("Unexpected error during conversion")

        return jsonify({
            "status": "FAILURE",
            "error": str(e)
        }), 500


def transform(document, business_type, documentType, listDocument, request_id, request_status):
    mapping = fetch_mapping_config(business_type)
    if not mapping:
        raise ValueError(
            f"No mapping configuration found for business type: {business_type}"
        ) 
    mapping_lookup = { m["titanFieldName"]: m for m in mapping }

    object_list_field = next((f for f in document["fields"] if f["type"] == "Object List"), None)
    groups = object_list_field["values"] if object_list_field else [[]] 
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

    output_documents = []
    for group_index, group in enumerate(groups):
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
        output_documents.append({
        **build_metadata(
            document,
            business_type,
            documentType,
            listDocument,
            request_id,
            request_status,
            group_index
        ),
        "fields": common_fields + group_fields,
        })
    return output_documents

if __name__ == "__main__":
    app.run(debug = True)