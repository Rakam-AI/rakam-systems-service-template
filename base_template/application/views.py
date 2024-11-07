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
    S3FileManagerUploadFoldersSerializer,
    S3FileManagerDownloadFilesSerializer,
    S3FileManagerListFilesSerializer,
    S3FileManagerUpdatePrefixSerializer,
    S3FileManagerEmptySerializer,
    LLMConnectorCallLLMSerializer,
    LLMConnectorCallLLMStreamSerializer,
    LLMConnectorCallLLMOutputJSONSerializer,
    SQLDBExcuteQuerySerializer,
    SQLDBUpdateDataSerializer,
    SQLDBInsertDataSerializer,
    SQLDBDeleteDataSerializer,
    SQLDBCreateTableSerializer,
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

@extend_schema(
    request=S3FileManagerUploadFoldersSerializer,
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
    description="Upload folders to an S3 bucket.",
    tags=["S3 File Manager"],
)
@api_view(["POST"])
def upload_folders(request):
    serializer = S3FileManagerUploadFoldersSerializer(data=request.data)
    if serializer.is_valid():
        local_path = serializer.validated_data.get("local_path")
        prefix = serializer.validated_data.get("prefix") or "test"
        
        components.s3_manager.upload_folders(local_path=local_path, prefix=prefix)
        
        return Response({"message": "Folders uploaded successfully.", "status": "success", "local_path": local_path, "prefix":prefix}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=S3FileManagerDownloadFilesSerializer,
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
    description="Download files from an S3 bucket.",
    tags=["S3 File Manager"],
)
@api_view(["POST"])
def download_files(request):
    serializer = S3FileManagerDownloadFilesSerializer(data=request.data)
    if serializer.is_valid():
        local_path = serializer.validated_data.get("local_path")
        
        components.s3_manager.download_files(local_path=local_path)
        
        return Response({"message": "Files downloaded successfully.", "status": "success", "local_path": local_path}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=S3FileManagerListFilesSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "folders": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="List files and folders in an S3 bucket.",
    tags=["S3 File Manager"],
)
@api_view(["POST"])
def list_files(request):
    serializer = S3FileManagerListFilesSerializer(data=request.data)
    if serializer.is_valid():
        prefix = serializer.validated_data.get("prefix")
        file_names, folders = components.s3_manager.get_file_folders(prefix=prefix)
        
        return Response({"files": file_names, "folders": folders}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=S3FileManagerUpdatePrefixSerializer,
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
    description="Update the prefix of files in an S3 bucket.",
    tags=["S3 File Manager"],
)
@api_view(["POST"])
def update_prefix(request):
    serializer = S3FileManagerUpdatePrefixSerializer(data=request.data)
    if serializer.is_valid():
        local_path = serializer.validated_data.get("local_path")
        prefix = serializer.validated_data.get("prefix")
        
        components.s3_manager.update_prefix(local_path=local_path, prefix=prefix)
        
        return Response({"message": "Prefix updated successfully.", "status": "success", "local_path": local_path, "prefix": prefix}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=S3FileManagerEmptySerializer,
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
    description="Empty an S3 bucket.",
    tags=["S3 File Manager"],
)
@api_view(["POST"])
def empty_s3(request):
    serializer = S3FileManagerEmptySerializer(data=request.data)
    if serializer.is_valid():
        prefix = serializer.validated_data.get("prefix")
        
        components.s3_manager.empty(prefix=prefix)
        
        return Response({"message": "S3 bucket emptied successfully.", "status": "success", "prefix": prefix}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=LLMConnectorCallLLMSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Call the LLM with the given system and user prompts.",
    tags=["LLM Connector"],
)
@api_view(["POST"])
def call_llm(request):
    serializer = LLMConnectorCallLLMSerializer(data=request.data)
    if serializer.is_valid():
        sys_prompt = serializer.validated_data.get("sys_prompt")
        prompt = serializer.validated_data.get("prompt")
        temperature = serializer.validated_data.get("temperature") or 0
        
        response = components.llm_connector.call_llm(sys_prompt=sys_prompt, prompt=prompt, temperature=temperature)
        
        return Response({"system_prompt":sys_prompt, "user_prompt": prompt,"response": response, "temperature": temperature}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=LLMConnectorCallLLMStreamSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Call the LLM with the given system and user prompts using streaming.",
    tags=["LLM Connector"],
)
@api_view(["POST"])
def call_llm_stream(request):
    serializer = LLMConnectorCallLLMStreamSerializer(data=request.data)
    if serializer.is_valid():
        sys_prompt = serializer.validated_data.get("sys_prompt")
        prompt = serializer.validated_data.get("prompt")
        temperature = serializer.validated_data.get("temperature") or 0
        seed = serializer.validated_data.get("seed") or 0
        
        response = components.llm_connector.call_llm_stream(sys_prompt=sys_prompt, prompt=prompt, temperature=temperature, seed=seed)
        
        return Response({"response": response}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=LLMConnectorCallLLMOutputJSONSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Call the LLM with the given system and user prompts and output in JSON format.",
    tags=["LLM Connector"],
)
@api_view(["POST"])
def call_llm_output_json(request):
    serializer = LLMConnectorCallLLMOutputJSONSerializer(data=request.data)
    if serializer.is_valid():
        sys_prompt = serializer.validated_data.get("sys_prompt")
        prompt = serializer.validated_data.get("prompt")
        temperature = serializer.validated_data.get("temperature") or 0
        seed = serializer.validated_data.get("seed") or 0
        
        response = components.llm_connector.call_llm_output_json(sys_prompt=sys_prompt, prompt=prompt, temperature=temperature, seed=seed)
        
        return Response({"response": response}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=SQLDBExcuteQuerySerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Execute a query on the SQL database.",
    tags=["SQL Database"],
)
@api_view(["POST"])
def SQLDBexecute_query(request):
    serializer = SQLDBExcuteQuerySerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data.get("query")
        params = serializer.validated_data.get("params")
        
        response = components.sql_db.execute_query(query=query, params=params)
        
        return Response({"response": response}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=SQLDBInsertDataSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Insert data into the SQL database.",
    tags=["SQL Database"],
)
@api_view(["POST"])
def SQLDBinsert_data(request):
    serializer = SQLDBInsertDataSerializer(data=request.data)
    if serializer.is_valid():
        table = serializer.validated_data.get("table")
        data = serializer.validated_data.get("data")
        
        components.sql_db.insert_data(table=table, data=data)
        
        return Response({"response": "Data inserted successfully."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=SQLDBUpdateDataSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Update data in the SQL database.",
    tags=["SQL Database"],
)
@api_view(["POST"])
def SQLDBupdate_data(request):
    serializer = SQLDBUpdateDataSerializer(data=request.data)
    if serializer.is_valid():
        table = serializer.validated_data.get("table")
        data = serializer.validated_data.get("data")
        condition = serializer.validated_data.get("condition")
        condition_params = serializer.validated_data.get("condition_params")
        
        components.sql_db.update_data(table=table, data=data, condition=condition, condition_params=condition_params)
        
        return Response({"response": "Data updated successfully."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=SQLDBDeleteDataSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Delete data from the SQL database.",
    tags=["SQL Database"],
)
@api_view(["POST"])
def SQLDBdelete_data(request):
    serializer = SQLDBDeleteDataSerializer(data=request.data)
    if serializer.is_valid():
        table = serializer.validated_data.get("table")
        condition = serializer.validated_data.get("condition")
        condition_params = serializer.validated_data.get("condition_params")
        
        components.sql_db.delete_data(table=table, condition=condition, condition_params=condition_params)
        
        return Response({"response": "Data deleted successfully."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=SQLDBCreateTableSerializer,
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="Bad Request"),
    },
    description="Create a table in the SQL database.",
    tags=["SQL Database"],
)
@api_view(["POST"])
def SQLDBcreate_table(request):
    serializer = SQLDBCreateTableSerializer(data=request.data)
    if serializer.is_valid():
        table = serializer.validated_data.get("table")
        columns = serializer.validated_data.get("columns")
        
        components.sql_db.create_table(table=table, columns=columns)
        
        return Response({"response": "Table created successfully."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
            }
        ),
    },
    description="Get data from the SQL database.",
    tags=["SQL Database"],
)
@api_view(["GET"])
def SQLDBshow_tables(request):
    response = components.sql_db.show_tables_with_content()
    
    # Convert the dictionary to a tuple of items to make it hashable
    hashable_response = tuple(response.items())
    
    return Response({"Tables": hashable_response}, status=status.HTTP_200_OK)