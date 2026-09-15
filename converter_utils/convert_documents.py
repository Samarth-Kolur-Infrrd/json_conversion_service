from common_utils.get_document_type import getType
from converter_utils.convertor import transform

def convert_document(data):
    output = []
    document_ids=[]
    transformed_data = []

    for document in data["documents"]:
        businessType = getType(document,"business")
        if not businessType:
            continue
        documentType =getType(document,"document")
        listDocument = getType(document,"list")

        transformed_data = transform(document, 
                                    businessType,
                                    documentType,
                                    listDocument,
                                    data["requestId"], 
                                    data["status"])
        print(transformed_data)
        document_ids.append(transformed_data[0]["document_id"])
        output.extend(transformed_data)
    return [output, document_ids]