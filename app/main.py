import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import json
from pydantic import ValidationError

import logging
from mongoDB.seed import customFormatTranslatedDocuments
from error_handling_utils.model import Request
from error_handling_utils.errorHandler import validation_exception_handler
from converter_utils.convert_documents import convert_document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_exception_handler(ValidationError, validation_exception_handler )


@app.post("/api/convert")
def convert(raw:str = Body(...,media_type="text/plain")):
    raw_data = json.loads(raw)
    data = json.loads(raw_data)

    request = Request.model_validate(data)
    document_output = convert_document(data)
    output, document_ids = document_output[0], document_output[1]
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
    uvicorn.run("app.main:app", reload=True, port=8001)
