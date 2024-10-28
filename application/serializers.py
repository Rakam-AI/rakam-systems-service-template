from rest_framework import serializers

class DataProcessorSerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=255)

class VectorStoreSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)

class VSManagerInjectSerializer(serializers.Serializer):
    pass  # Assuming no input fields are needed

class RAGSerializer(serializers.Serializer):
    test_query = serializers.CharField(required=True, max_length=255)
