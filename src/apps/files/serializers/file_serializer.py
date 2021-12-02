from rest_framework.serializers import ModelSerializer

from src.apps.files.models import File


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'description', 'type', 'size')
        read_only_fields = ('id', 'name', 'type', 'size')
