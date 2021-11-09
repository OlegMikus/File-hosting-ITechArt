from rest_framework.serializers import ModelSerializer

from src.apps.files.models import File


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ('name', 'description')
        read_only_fields = ('name', )
