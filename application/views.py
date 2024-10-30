from application.engine import components
from application.serializers import (
    DataProcessorSerializer,
    VectorStoreSearchSerializer,
    VectorStoreGetSizeSerializer,
    VSManagerInjectSerializer,
    VSManagerAddSerializer,
    SimpleGenerationSerializer,
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
    description="Process data from a given directory path to VS files.",
    tags=["Data Processor"],
)
@api_view(["POST"])
def process_from_directory(request):
    serializer = DataProcessorSerializer(data=request.data)
    if serializer.is_valid():
        directory = serializer.validated_data.get("directory")
        response = components.data_processor.call_main(directory_path=directory)
        return Response(response, status=status.HTTP_200_OK)        
            
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
        collection_name = serializer.validated_data.get("collection_name") or "base"
        query = serializer.validated_data.get("query")
        base_response = components.VS.call_main(query=query,collection_name=collection_name)
        return Response(base_response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=VectorStoreGetSizeSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "size": {"type": "integer"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Get the size and nodes of a collection in the vector store.",
    tags=["Vector Store"],
)
@api_view(["POST"])
def get_nodes(request):
    serializer = VectorStoreGetSizeSerializer(data=request.data)
    if serializer.is_valid():
        collection_name = serializer.validated_data.get("collection_name") or "base"
        base_response = components.VS.call_get_nodes(collection_name=collection_name)
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
    description="Inject collection from data in a directory into the vector store.",
    tags=["Vector Store Manager"],
)
@api_view(["POST"])
def vs_manager_inject(request):
    serializer = VSManagerInjectSerializer(data=request.data)
    if serializer.is_valid():
        directory = serializer.validated_data.get("directory")
        collection_name = serializer.validated_data.get("collection_name") or "base"
        
        base_response = components.vsManager.call_create_from_directory(
            directory_path=directory,
            collection_name=collection_name
        )
        
        if base_response is None:
            # Return a 500 error with a custom message if no response is returned
            return Response(
                {"message": "Collection creation failed to provide a response.", "status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({"message": "Files injected successfully.", "status": "success", "files": base_response}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=VSManagerAddSerializer,
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
    description="Add documents from a directory to an existing collection in the vector store.",
    tags=["Vector Store Manager"],
)
@api_view(["POST"])
def vs_manager_add_files(request):
    serializer = VSManagerAddSerializer(data=request.data)
    if serializer.is_valid():
        directory = serializer.validated_data.get("directory")
        collection_name = serializer.validated_data.get("collection_name") or "base"
        
        # Call the new function to add files to the collection
        base_response = components.vsManager.call_add_vsfiles(
            directory_path=directory,
            collection_name=collection_name
        )
        
        if base_response is None:
            return Response(
                {"message": "Adding files to the collection failed.", "status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({"message": "Files added successfully.", "status": "success", "files": base_response}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=SimpleGenerationSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "generated_text": {"type": "string"},
                    "query": {"type": "string"},
                    "status": {"type": "string"},
                },
            },
            description="The generated text response based on the input query."
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Generate text using LLM based on the provided query.",
    tags=["Simple Generator"],
)
@api_view(["POST"])
def simple_generation(request):
    serializer = SimpleGenerationSerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data.get("query")
        generated_text = components.generator.call_direct_generation(query=query)
        response_data = {
            "generated_text": generated_text,
            "query": query,
            "status": "success",
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
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
    tags=["RAG Generator"],
)
@api_view(["POST"])
def rag(request):
    serializer = RAGSerializer(data=request.data)
    if serializer.is_valid():
        test_query = serializer.validated_data.get("test_query")
        base_response = components.ragGen.test(test_query=test_query)
        return Response(base_response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
