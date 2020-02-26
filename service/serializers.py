import io
import json

from rest_framework import serializers

from service.domain import InputFile, OutputFile


class InputFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    filename = serializers.CharField()

    def create(self, validated_data):
        return InputFile(
            raw_file=validated_data["file"], filename=validated_data["filename"]
        )

    def update(self, instance, validated_data):
        pass


class OutputFileSerializer(serializers.Serializer):
    compressed_file = serializers.FileField()
    filename = serializers.CharField()

    def create(self, validated_data):
        return OutputFile(
            compressed_file=validated_data["file"], filename=validated_data["filename"]
        )

    def update(self, instance, validated_data):
        pass
