from django.urls import path

from . import DocumentViews

urlpatterns = [
	path('add_document/', DocumentViews.add_document, name='add document'),
	path('get_user_documents/', DocumentViews.get_user_documents, name='get user documents'),
	path('delete_document/', DocumentViews.delete_document, name='delete document'),
	path('get_document_from_id/', DocumentViews.get_document_from_id, name='get document from id'),
	path('get_documents_by_type/', DocumentViews.get_documents_by_type, name='get documents by type')
]