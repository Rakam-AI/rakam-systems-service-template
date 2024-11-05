from rest_framework import serializers

class DataProcessorDirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=1024)

class DataProcessorFileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=1024)

class VectorStoreSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=1024)
    collection_name = serializers.CharField(required=False, max_length=1024, default="base")

class VectorStoreGetNodesSerializer(serializers.Serializer):
    collection_name = serializers.CharField(required=False, max_length=1024, default="base")
    
class VSManagerBuildFromDirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=1024)
    collection_name = serializers.CharField(required=False, max_length=1024, default="base")

class VSManagerBuildFromFileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=1024)
    collection_name = serializers.CharField(required=False, max_length=1024, default="base")

class VSManagerAddFromDirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=1024)
    collection_name = serializers.CharField(required=False, max_length=1024, default="base")

class VSManagerAddFromFileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=1024)
    collection_name = serializers.CharField(required=False, max_length=1024, default="base")

class RAGGenerationSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=1024)

class RAGGenerationSplitQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=1024)

class RAGGenerationSplitQueryResponseSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=1024)

class S3FileManagerUploadFoldersSerializer(serializers.Serializer):
    local_path = serializers.CharField(required=True, max_length=1024)
    prefix = serializers.CharField(required=False, max_length=1024, default="test")

class S3FileManagerDownloadFilesSerializer(serializers.Serializer):
    local_path = serializers.CharField(required=False, max_length=1024, default=None)

class S3FileManagerListFilesSerializer(serializers.Serializer):
    prefix = serializers.CharField(required=False, max_length=1024, default=None)

class S3FileManagerUpdatePrefixSerializer(serializers.Serializer):
    local_path = serializers.CharField(required=True, max_length=1024)
    prefix = serializers.CharField(required=True, max_length=1024)

class S3FileManagerEmptySerializer(serializers.Serializer):
    prefix = serializers.CharField(required=False, max_length=1024, default=None)

class LLMConnectorCallLLMSerializer(serializers.Serializer):
    sys_prompt = serializers.CharField(required=True, max_length=1024)
    prompt = serializers.CharField(required=True, max_length=8192)
    temperature = serializers.FloatField(required=False, default=0)

class LLMConnectorCallLLMStreamSerializer(serializers.Serializer):
    sys_prompt = serializers.CharField(required=True, max_length=1024)
    prompt = serializers.CharField(required=True, max_length=8192)
    temperature = serializers.FloatField(required=False, default=0)
    seed = serializers.IntegerField(required=False, default=0)

class LLMConnectorCallLLMOutputJSONSerializer(serializers.Serializer):
    sys_prompt = serializers.CharField(required=True, max_length=1024)
    prompt = serializers.CharField(required=True, max_length=8192)
    temperature = serializers.FloatField(required=False, default=0)
    seed = serializers.IntegerField(required=False, default=0)

class SQLDBExcuteQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=8192)
    params = serializers.ListField(required=False, default=None)

class SQLDBInsertDataSerializer(serializers.Serializer):
    table = serializers.CharField(required=True, max_length=1024)
    data = serializers.DictField(required=True)

class SQLDBUpdateDataSerializer(serializers.Serializer):
    table = serializers.CharField(required=True, max_length=1024)
    data = serializers.DictField(required=True)
    condition = serializers.CharField(required=True, max_length=8192)
    condition_params = serializers.ListField(required=True)

class SQLDBDeleteDataSerializer(serializers.Serializer):
    table = serializers.CharField(required=True, max_length=1024)
    condition = serializers.CharField(required=True, max_length=8192)
    condition_params = serializers.ListField(required=True)

class SQLDBCreateTableSerializer(serializers.Serializer):
    table = serializers.CharField(required=True, max_length=1024)
    columns = serializers.CharField(required=True, max_length=8192)
