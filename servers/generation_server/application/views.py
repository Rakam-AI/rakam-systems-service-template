from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

@api_view(['GET'])
def call_llm(request):
    serializer = LLMManagerCallllmSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    sys_prompt=request.query_params['sys_prompt'], prompt=request.query_params['prompt'], temperature=str(request.query_params.get('temperature', '0.5'))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def call_llm_stream(request):
    serializer = LLMManagerCallllmstreamSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    sys_prompt=request.query_params['sys_prompt'], prompt=request.query_params['prompt'], temperature=str(request.query_params.get('temperature', '0.5'))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def call_llm_output_json(request):
    serializer = LLMManagerCallllmoutputjsonSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    sys_prompt=request.query_params['sys_prompt'], prompt=request.query_params['prompt'], temperature=str(request.query_params.get('temperature', '0.5'))
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def rag_generate(request):
    serializer = RAGGeneratorRaggenerateSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    query=request.query_params['query']
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def split_query(request):
    serializer = RAGGeneratorSplitquerySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    query=request.query_params['query']
    return Response({'status': 'success', 'data': 'Your data here'})

@api_view(['GET'])
def rag_generate_split_query(request):
    serializer = RAGGeneratorRaggeneratesplitquerySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    query=request.query_params['query']
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

