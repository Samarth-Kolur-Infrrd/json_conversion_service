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

