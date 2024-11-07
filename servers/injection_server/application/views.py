from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

@api_view(['GET'])
def process_from_directory(request):
    serializer = DataProcessorProcessfromdirectorySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    directory=request.query_params['directory']
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def process_from_file(request):
    serializer = DataProcessorProcessfromfileSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    file_path=request.query_params['file_path']
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def build_from_directory(request):
    serializer = VSManagerBuildfromdirectorySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    directory=request.query_params['directory'], collection_name=str(request.query_params.get('collection_name', 'base'))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def build_from_file(request):
    serializer = VSManagerBuildfromfileSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    file_path=request.query_params['file_path'], collection_name=str(request.query_params.get('collection_name', 'base'))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def add_from_directory(request):
    serializer = VSManagerAddfromdirectorySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    directory=request.query_params['directory'], collection_name=str(request.query_params.get('collection_name', 'base'))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def add_from_file(request):
    serializer = VSManagerAddfromfileSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    file_path=request.query_params['file_path'], collection_name=str(request.query_params.get('collection_name', 'base'))
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

