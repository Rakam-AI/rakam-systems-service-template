from application.engine import components
from application.serializers import (
    DataProcessorDirectorySerializer,
    DataProcessorFileSerializer,
    VectorStoreSearchSerializer,
    VectorStoreGetNodesSerializer,
    VSManagerBuildFromDirectorySerializer,
    VSManagerBuildFromFileSerializer,
    VSManagerAddFromDirectorySerializer,
    VSManagerAddFromFileSerializer,
    RAGGenerationSerializer,
    RAGGenerationSplitQuerySerializer,
    RAGGenerationSplitQueryResponseSerializer,
)

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@extend_schema(
    request=DataProcessorDirectorySerializer,
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
    serializer = DataProcessorDirectorySerializer(data=request.data)
    if serializer.is_valid():
        directory = serializer.validated_data.get("directory")
        response = components.data_processor.call_main(directory_path=directory)
        return Response(response, status=status.HTTP_200_OK)        
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=DataProcessorFileSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "result": {"type": "string"},
                    "details": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string"},
                            "status": {"type": "string"},
                        },
                    },
                },
            },
            description="The processing result from the given file."
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Process data from a given file path to a VS file.",
    tags=["Data Processor"],
)
@api_view(["POST"])
def process_from_file(request):
    serializer = DataProcessorFileSerializer(data=request.data)
    if serializer.is_valid():
        file_path = serializer.validated_data.get("file_path")
        response = components.data_processor.call_process_file(file_path=file_path)
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
    request=VectorStoreGetNodesSerializer,
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
    serializer = VectorStoreGetNodesSerializer(data=request.data)
    if serializer.is_valid():
        collection_name = serializer.validated_data.get("collection_name") or "base"
        base_response = components.VS.call_get_nodes(collection_name=collection_name)
        return Response(base_response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=VSManagerBuildFromDirectorySerializer,
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
    description="Build collection from data in a directory into the vector store.",
    tags=["Vector Store Manager"],
)
@api_view(["POST"])
def vs_manager_build_from_directory(request):
    serializer = VSManagerBuildFromDirectorySerializer(data=request.data)
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
        
        return Response({"message": "Files injected successfully.", "Length of Nodes": len(base_response[0]["nodes"]), "files": base_response}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=VSManagerBuildFromFileSerializer,
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
    description="Build collection from data in a file into the vector store.",
    tags=["Vector Store Manager"],
)
@api_view(["POST"])
def vs_manager_build_from_file(request):
    serializer = VSManagerBuildFromFileSerializer(data=request.data)
    if serializer.is_valid():
        file_path = serializer.validated_data.get("file_path")
        collection_name = serializer.validated_data.get("collection_name") or "base"
        
        base_response = components.vsManager.call_create_from_file(
            file_path=file_path,
            collection_name=collection_name
        )
        
        if base_response is None:
            return Response(
                {"message": "Collection creation failed to provide a response.", "status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({"message": "Files injected successfully.", "Length of Nodes": len(base_response[0]["nodes"]), "files": base_response}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=VSManagerAddFromDirectorySerializer,
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
def vs_manager_add_from_directory(request):
    serializer = VSManagerAddFromDirectorySerializer(data=request.data)
    if serializer.is_valid():
        directory = serializer.validated_data.get("directory")
        collection_name = serializer.validated_data.get("collection_name") or "base"
        
        # Call the new function to add files to the collection
        base_response = components.vsManager.call_add_from_directory(
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
    request=VSManagerAddFromFileSerializer,
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
    description="Add documents from a file to an existing collection in the vector store.",
    tags=["Vector Store Manager"],
)
@api_view(["POST"])
def vs_manager_add_from_file(request):
    serializer = VSManagerAddFromFileSerializer(data=request.data)
    if serializer.is_valid():
        file_path = serializer.validated_data.get("file_path")
        collection_name = serializer.validated_data.get("collection_name") or "base"
        
        # Call the new function to add files to the collection
        base_response = components.vsManager.call_add_from_file(
            file_path=file_path,
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
    request=RAGGenerationSerializer,
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
    description="Generate text using RAG based on the provided query.",
    tags=["RAG Generator"],
)
@api_view(["POST"])
def rag_generation(request):
    serializer = RAGGenerationSerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data.get("query")
        generated_text = components.ragGenerator.call_main(query=query)
        
        return Response(generated_text, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=RAGGenerationSplitQuerySerializer,
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
    description="Split the input query into multiple queries and return a list of sub-queries.",
    tags=["RAG Generator"],
)
@api_view(["POST"])
def rag_generation_split_query(request):
    serializer = RAGGenerationSplitQuerySerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data.get("query")
        generated_text = components.ragGenerator.call_split_query(query=query)
        
        return Response(generated_text, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=RAGGenerationSplitQueryResponseSerializer,
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
    description="RAG with split query strategy.",
    tags=["RAG Generator"],
)
@api_view(["POST"])
def rag_generation_split_query_response(request):
    serializer = RAGGenerationSplitQueryResponseSerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data.get("query")
        generated_text = components.ragGenerator.call_rag_with_split_query(query=query)
        
        return Response(generated_text, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)