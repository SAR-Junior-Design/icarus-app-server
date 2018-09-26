from schema import And

class DocumentViewSchemas:
    add_document_schema = {
        "location": And(str),
        "type": And(str)
    }

    document_id_schema = {
        "id": And(str)
    }

    document_type_schema = {
        "type": And(str)
    }