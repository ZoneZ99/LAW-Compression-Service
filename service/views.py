import os

import requests
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.serializers import InputFileSerializer
from service.utils import process_uploaded_file

load_dotenv()


class CompressFileView(APIView):
    def post(self, request, **params):
        input_file_serializer = InputFileSerializer(data=request.data)
        if input_file_serializer.is_valid():
            input_file = input_file_serializer.save()
            original_file_data = {
                "name": input_file.filename,
                "ext": input_file.filename.split(".")[-1],
                "size": input_file.raw_file.size
            }
            file_metadata, file_url = process_uploaded_file(input_file.raw_file)
            try:
                metadata_service_response = self.call_metadata_service(
                    original_file_data,
                    file_metadata,
                    file_url
                )
                return Response(
                    data=metadata_service_response.json(), status=status.HTTP_200_OK
                )
            except:
                return Response(
                    data={"message": "something wrong happeneded"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                data=input_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def call_metadata_service(self, original_file_data, file_metadata, file_url):
        METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL")
        metadata_service_response = requests.post(
            url=f"{METADATA_SERVICE_URL}metadata/",
            data={
                "name": original_file_data["name"],
                "type": original_file_data["ext"],
                "size": original_file_data["size"],
                "location": file_url,
                "updated": file_metadata.client_modified,
            },
        )
        return metadata_service_response
