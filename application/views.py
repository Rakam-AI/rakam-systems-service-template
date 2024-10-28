from application.engine import components
from application.serializers import (
    DataProcessorSerializer,
    VectorStoreSearchSerializer,
    VSManagerInjectSerializer,
    RAGSerializer,
)

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@extend_schema(
    request=DataProcessorSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "result": {"type": "string"},
                    "details": {
                        "type": "object",
                        "properties": {
                            "file_count": {"type": "integer"},
                            "processed_files": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "status": {"type": "string"},
                        },
                    },
                },
            },
            description="The processing result from the given directory."
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Process data from a given directory path.",
    tags=["Data Processor"],
)
@api_view(["POST"])
def dataprocessor(request):
    serializer = DataProcessorSerializer(data=request.data)
    if serializer.is_valid():
        directory = serializer.validated_data.get("directory")
        base_response = components.processor.test(directory_path=directory)
        return Response(base_response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=VectorStoreSearchSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item": {"type": "string"},
                                "score": {"type": "number"},
                            },
                        },
                    },
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Search for items in the vector store using a query.",
    tags=["Vector Store"],
)
@api_view(["POST"])
def search_vector_store(request):
    serializer = VectorStoreSearchSerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data.get("query")
        base_response = components.VS.test(query=query)
        return Response(base_response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=VSManagerInjectSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "status": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Inject data into the vector store manager.",
    tags=["Vector Store Manager"],
)
@api_view(["POST"])
def vs_manager_inject(request):
    serializer = VSManagerInjectSerializer(data=request.data)
    if serializer.is_valid():
        base_response = components.vsManager.test()
        return Response(base_response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=RAGSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "generated_text": {"type": "string"},
                    "confidence_score": {"type": "number"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Retrieve answers using a Retrieval-Augmented Generation (RAG) approach.",
    tags=["RAG"],
)
@api_view(["POST"])
def rag(request):
    serializer = RAGSerializer(data=request.data)
    if serializer.is_valid():
        test_query = serializer.validated_data.get("test_query")
        base_response = components.ragGen.test(test_query=test_query)
        return Response(base_response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
