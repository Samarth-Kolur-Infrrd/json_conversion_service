import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import json
from pydantic import ValidationError

import logging
from seed import customFormatTranslatedDocuments
from convertor import transform
from model import Request
from errorHandler import validation_exception_handler
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_exception_handler(ValidationError, validation_exception_handler )

def getType(document,type):
    if type == "business":
        return next((m["value"] 
                    for m in document["docTypeHierarchy"] 
                    if m["classificationName"] == "CollateralType"),None)
    if type == "document":
        return next(m["value"] 
                        for m in document["docTypeHierarchy"] 
                        if m["classificationName"] == "DocumentType")
    if type == "list":
        return any(m["classificationName"] == "LIST_TYPE" and (m["value"] == "LIST" or m["value"] == "LIIST")
                            for m in document["docTypeHierarchy"])


@app.post("/api/convert")
def convert(raw:str = Body(...,media_type="text/plain")):
    raw_data = json.loads(raw)
    data = json.loads(raw_data)

    request = Request.model_validate(data)

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
     
    customFormatTranslatedDocuments(output)
    return JSONResponse(
        status_code=200,
        content = {
            "status":"SUCCESS",
            "upload_request_id": output[0]["upload_request_id"],
            "documents_converted": len(output),
            "document_ids":document_ids
        }
    )

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)