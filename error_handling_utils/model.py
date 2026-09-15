from pydantic import BaseModel, field_validator, model_validator

class Request(BaseModel):
    requestId: str
    status: str
    documents: list

    @model_validator(mode="before")
    @classmethod
    def validate_request(cls, data):

        if "requestId" not in data or not data["requestId"]:
            raise ValueError("requestId is missing")

        if "status" not in data or not data["status"]:
            raise ValueError("status is missing")

        if "documents" not in data or not data["documents"]:
            raise ValueError("documents is missing")

        return data

class MappingCheck(BaseModel):
    mapping: list

    @field_validator("mapping")
    @classmethod
    def validate_mapping(cls, value):
        if not value:
            raise ValueError("Mapping configuration is missing or empty")
        return value