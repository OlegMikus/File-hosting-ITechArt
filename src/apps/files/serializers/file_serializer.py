from rest_framework.serializers import ModelSerializer

from src.apps.files.models import File


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ('name', 'description', 'is_alive', 'date_updated')
        read_only_fields = ('name', )
