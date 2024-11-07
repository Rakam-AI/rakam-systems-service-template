from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

@api_view(['GET'])
def search(request):
    serializer = VectorStoreSearchSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    query=request.query_params['query'], collection_name=str(request.query_params.get('collection_name', 'base'))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def get_nodes(request):
    serializer = VectorStoreGetnodesSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    collection_name=str(request.query_params.get('collection_name', 'base'))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def upload_folders(request):
    serializer = S3FileManagerUploadfoldersSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    local_path=request.query_params['local_path'], prefix=str(request.query_params.get('prefix', ''))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def download_files(request):
    serializer = S3FileManagerDownloadfilesSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    local_path=request.query_params['local_path']
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def list_files(request):
    serializer = S3FileManagerListfilesSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    prefix=request.query_params['prefix']
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def update_prefix(request):
    serializer = S3FileManagerUpdateprefixSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    local_path=request.query_params['local_path'], prefix=request.query_params['prefix']
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def empty_prefix(request):
    serializer = S3FileManagerEmptyprefixSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    prefix=request.query_params['prefix']
    return Response({'status': 'success', 'data': 'Your data here'})

