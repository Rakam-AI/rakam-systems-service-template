from rest_framework import serializers

class LLMManagerCallllmSerializer(serializers.Serializer):
    sys_prompt = serializers.CharField(required=True, max_length=1024)
    prompt = serializers.CharField(required=True, max_length=8192)
    temperature = serializers.CharField(required=False, max_length=128, default=0.5)

class LLMManagerCallllmstreamSerializer(serializers.Serializer):
    sys_prompt = serializers.CharField(required=True, max_length=1024)
    prompt = serializers.CharField(required=True, max_length=8192)
    temperature = serializers.CharField(required=False, max_length=128, default=0.5)

class LLMManagerCallllmoutputjsonSerializer(serializers.Serializer):
    sys_prompt = serializers.CharField(required=True, max_length=1024)
    prompt = serializers.CharField(required=True, max_length=8192)
    temperature = serializers.CharField(required=False, max_length=128, default=0.5)

class RAGGeneratorRaggenerateSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=128)

class RAGGeneratorSplitquerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=128)

class RAGGeneratorRaggeneratesplitquerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=128)

class S3FileManagerUploadfoldersSerializer(serializers.Serializer):
    local_path = serializers.CharField(required=True, max_length=128)
    prefix = serializers.CharField(required=False, max_length=128, default='')

class S3FileManagerDownloadfilesSerializer(serializers.Serializer):
    local_path = serializers.CharField(required=True, max_length=128)

class S3FileManagerListfilesSerializer(serializers.Serializer):
    prefix = serializers.CharField(required=True, max_length=128)

class S3FileManagerUpdateprefixSerializer(serializers.Serializer):
    local_path = serializers.CharField(required=True, max_length=128)
    prefix = serializers.CharField(required=True, max_length=128)

class S3FileManagerEmptyprefixSerializer(serializers.Serializer):
    prefix = serializers.CharField(required=True, max_length=128)

