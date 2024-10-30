from rest_framework import serializers

class DataProcessorSerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)

class VectorStoreSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class VectorStoreGetSizeSerializer(serializers.Serializer):
    collection_name = serializers.CharField(required=False, max_length=255, default="base")
    
class VSManagerInjectSerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class VSManagerAddSerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)
    collection_name = serializers.CharField(required=False, max_length=255, default="base")

class SimpleGenerationSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)

class RAGSerializer(serializers.Serializer):
    test_query = serializers.CharField(required=True, max_length=255)
