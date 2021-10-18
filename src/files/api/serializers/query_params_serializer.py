from rest_framework import serializers


class ChunkUploadQueryParamsSerializer(serializers.Serializer):

    resumableTotalChunks = serializers.IntegerField(required=True, min_value=1)
    resumableChunkNumber = serializers.IntegerField(required=True, min_value=1)
    resumableFilename = serializers.CharField(max_length=256, required=True)
    resumableIdentifier = serializers.CharField(max_length=128, required=True)
