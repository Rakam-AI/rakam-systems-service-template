from rest_framework import serializers

class DataProcessorProcessfromdirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=128)

class DataProcessorProcessfromfileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=128)

class VSManagerBuildfromdirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=128)
    collection_name = serializers.CharField(required=False, max_length=128, default='base')

class VSManagerBuildfromfileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=128)
    collection_name = serializers.CharField(required=False, max_length=128, default='base')

class VSManagerAddfromdirectorySerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, max_length=128)
    collection_name = serializers.CharField(required=False, max_length=128, default='base')

class VSManagerAddfromfileSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, max_length=128)
    collection_name = serializers.CharField(required=False, max_length=128, default='base')

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

