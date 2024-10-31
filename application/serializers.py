from rest_framework import serializers

class DataProcessorSerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)

class VectorStoreSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class VectorStoreGetSizeSerializer(serializers.Serializer):
    collection_name = serializers.CharField(required=False, max_length=255, default="base")
    
class VSManagerBuildSerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class VSManagerAddSerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class RAGGenerationSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)