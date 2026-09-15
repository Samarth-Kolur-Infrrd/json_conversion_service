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

