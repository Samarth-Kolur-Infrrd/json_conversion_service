from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["json_conversion_service"]

with open("field_names_mappings.json","r") as map:
    mappings = json.load(map)

FieldTransformationConfig = db["field_transformation_config"]
customFormatTranslatedDocumentDB = db["custom_format_translated_documents"]

def seeding():
    FieldTransformationConfig.insert_one({
        "business_type":"AUTO",
        "mappings" : mappings["autoFieldTransformationConfig"]
    })

    FieldTransformationConfig.insert_one({
        "business_type":"MORTGAGE",
        "mappings" : mappings["mortgageFieldTransformationConfig"]
    })

def fetch_mapping_config(business_type):
    
    fetchedFieldTransformationConfig = FieldTransformationConfig.find_one({"business_type":business_type})
    return fetchedFieldTransformationConfig["mappings"]

def customFormatTranslatedDocuments(output):
    customFormatTranslatedDocumentDB.insert_one({
        "customFormatTranslatedDocument": output
    })

fetch_mapping_config("AUTO")