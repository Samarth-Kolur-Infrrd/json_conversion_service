import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
