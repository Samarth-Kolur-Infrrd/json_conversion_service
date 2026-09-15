from mongoDB.seed import fetch_mapping_config
from error_handling_utils.model import MappingCheck


def build_mapping(business_type):
    mapping = fetch_mapping_config(business_type)
    request = MappingCheck.model_validate({"mapping":mapping})
    mapping_lookup = { m["titanFieldName"]: m for m in mapping }
    return mapping_lookup
