from .DocumentModel import Document
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from icarus_backend.document.DocumentViewSchemas import DocumentViewSchemas
from icarus_backend.utils import validate_body
import uuid
import json

@protected_resource()
@api_view(['POST'])
@validate_body(DocumentViewSchemas.add_document_schema)
def add_document(request):
    user = request.user
    request = request.data
    location = request['location']
    type = request['type']
    id = uuid.uuid4()
    document = Document(id=id, owner=user, type=type, location=location)
    document.save()

    response_data = {'id': id}
    response_json = json.dumps(response_data, cls=DjangoJSONEncoder)

    return HttpResponse(response_json, content_type = "application/json")

@protected_resource()
@api_view(['GET'])
def get_user_documents(request):
    user = request.user
    documents = Document.objects.filter(owner=user)

    documents_list = []
    for document in documents:
        document_dict = {}
        document_dict['id'] = document.id
        document_dict['owner'] = document.owner.username
        document_dict['location'] = document.location
        document_dict['type'] = document.type
        documents_list.append(document_dict)
    response_json = json.dumps(documents_list, sort_keys=True, indent=4, separators=(',', ': '))
    return HttpResponse(response_json, content_type = "application/json")

@protected_resource()
@api_view(['POST'])
@validate_body(DocumentViewSchemas.document_id_schema)
def delete_document(request):
    user = request.user
    request = request.data
    id = request['id']
    document = Document.objects.get(id=id)
    document.delete()

    response_data = {'message': 'Successfully removed document.'}
    response_json = json.dumps(response_data, cls=DjangoJSONEncoder)
    return HttpResponse(response_json, content_type = "application/json")

@protected_resource()
@api_view(['POST'])
@validate_body(DocumentViewSchemas.document_id_schema)
def get_document_from_id(request):
    request = request.data
    id = request['id']
    document = Document.objects.get(id=id)
    if document is None:
        response_data = {'message': "Bad document id."}
        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return HttpResponse(return_string, content_type = "application/json")
    response_data = {'id': document.id, 'owner': document.owner.username, 'location': document.location, 'type': document.type}
    response_json = json.dumps(response_data, cls=DjangoJSONEncoder)
    return HttpResponse(response_json, content_type = 'application/json')

@protected_resource()
@api_view(['POST'])
@validate_body(DocumentViewSchemas.document_type_schema)
def get_documents_by_type(request):
    request = request.data
    type = request['type']
    documents = Document.objects.filter(type=type)

    documents_list = []
    for document in documents:
        document_dict = {}
        document_dict['id'] = document.id
        document_dict['owner'] = document.owner.username
        document_dict['location'] = document.location
        document_dict['type'] = document.type
        documents_list.append(document_dict)
    response_json = json.dumps(documents_list, sort_keys=True, indent=4, separators=(',', ': '))
    return HttpResponse(response_json, content_type = "application/json")
