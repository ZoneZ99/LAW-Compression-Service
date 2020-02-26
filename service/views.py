from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.serializers import InputFileSerializer, OutputFileSerializer
from service.utils import compress_file


class CompressFileView(APIView):
    def post(self, request, **params):
        input_file_serializer = InputFileSerializer(data=request.data)
        if input_file_serializer.is_valid():
            input_file = input_file_serializer.save()
            compressed_file = compress_file(input_file.raw_file)
            return Response(
                data=OutputFileSerializer(instance=compressed_file).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=input_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
