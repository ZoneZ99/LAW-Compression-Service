import gzip
import io
import os

import dropbox
from dotenv import load_dotenv
from dropbox.files import WriteMode

load_dotenv()


def compress_file(raw_file):
    filename = f"{raw_file.name}.gz"
    compressed_file_bytes = io.BytesIO()
    with gzip.GzipFile(
        filename=filename, mode="wb", fileobj=compressed_file_bytes
    ) as compression:
        compression.write(raw_file.read())
    return compressed_file_bytes, filename


def upload_file(compressed_file_bytes, filename):
    dbx = dropbox.Dropbox(oauth2_access_token=os.getenv("DROPBOX_ACCESS_TOKEN"))
    file_path = f"/LAW/{filename}"
    file_metadata = dbx.files_upload(
        f=compressed_file_bytes.getvalue(), mode=WriteMode.overwrite, path=file_path
    )
    link = dbx.sharing_create_shared_link(path=file_metadata.path_display)
    return file_metadata, link.url


def process_uploaded_file(raw_file):
    compressed_file_bytes, filename = compress_file(raw_file)
    file_metadata, url = upload_file(compressed_file_bytes, filename)
    return file_metadata, url
