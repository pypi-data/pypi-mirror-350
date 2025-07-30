from scoutsdk.shared.conversations_types import SignedUploadUrlResponse
from scoutsdk.shared.upload_files import upload_file


def upload_file_to_signed_url(
    signed_url_response: SignedUploadUrlResponse,
    file_path: str,
    file_key: str | None = None,
) -> int:
    if file_key is None:
        file_key = file_path.split("/")[-1]

    return upload_file(signed_url_response, file_path, file_key)
