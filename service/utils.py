import gzip
import io

from service.domain import OutputFile


def compress_file(raw_file):
    filename = f"{raw_file.name}.gz"
    file_object = io.BytesIO()
    with gzip.GzipFile(
        filename=filename, mode="wb", fileobj=file_object
    ) as compression:
        compression.write(raw_file.read())
    return OutputFile(compressed_file=file_object, filename=filename)
