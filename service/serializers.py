from rest_framework import serializers

from service.domain import InputFile


class InputFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    filename = serializers.CharField()

    def create(self, validated_data):
        return InputFile(
            raw_file=validated_data["file"], filename=validated_data["filename"]
        )

    def update(self, instance, validated_data):
        pass
