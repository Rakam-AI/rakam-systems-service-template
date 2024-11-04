from rest_framework import serializers

class DataProcessorDirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)

class DataProcessorFileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=255)

class VectorStoreSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class VectorStoreGetNodesSerializer(serializers.Serializer):
    collection_name = serializers.CharField(required=False, max_length=255, default="base")
    
class VSManagerBuildFromDirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class VSManagerBuildFromFileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class VSManagerAddFromDirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class VSManagerAddFromFileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class RAGGenerationSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)

class RAGGenerationSplitQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)

class RAGGenerationSplitQueryResponseSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)