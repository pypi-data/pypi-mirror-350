import logging


def upload_file_on_gcs(
    client: object,
    bucket_name: str,
    source_file_name: str,
    destination_blob_name: str,
) -> None:
    """
    Uploads file on a GCP bucket.

    :type client: object
    :param client:
        The GCP client.

    :type bucket_name: str
    :param bucket_name:
        Name of the GCP bucket.

    :type source_file_name: str
    :param source_file_name:
        The file to upload.

    :type destination_blob_name: str
    :param destination_blob_name:
        The name of the file in the GCP bucket.

    :return None:
    """
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        logging.info(f"File: {source_file_name} uploaded to GCS.")

    except:
        logging.exception(
            f"Exception while trying to upload file: {source_file_name} to GCS."
        )
