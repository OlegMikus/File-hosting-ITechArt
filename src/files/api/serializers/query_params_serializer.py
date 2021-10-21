from rest_framework import serializers


class ChunkUploadQueryParamsSerializer(serializers.Serializer):

    resumableTotalChunks = serializers.IntegerField(source='total_chunks', min_value=1)
    resumableChunkNumber = serializers.IntegerField(source='chunk_number', min_value=1)
    resumableFilename = serializers.CharField(source='filename', max_length=256)
    resumableIdentifier = serializers.CharField(source='identifier', max_length=256)
    resumableType = serializers.CharField(source='extension', max_length=256)
    resumableTotalSize = serializers.CharField(source='total_size', max_length=256)
    resumableHash = serializers.CharField(source='hash_sum', max_length=32)
    resumableDescription = serializers.CharField()
