import logging


def upload_file_to_s3(
    client: object, bucket_name: str, file_bytes: bytes, object_name: str
) -> None:
    """
    Uploads file to an S3 bucket.

    :type client: object
    :param client:
        Boto3 S3 client.

    :type bucket_name: str
    :param bucket_name:
        Name of the S3 bucket.

    :type file_bytes: bytes
    :param file_bytes:
        Image bytes to upload.

    :type object_name: str
    :param object_name:
        Name for the object in S3.

    :return None:
    """
    try:
        logging.info(
            f"Uploading file to S3 bucket: {bucket_name}, object name: {object_name}"
        )
        client.upload_fileobj(file_bytes, bucket_name, object_name)
        logging.info(f"File uploaded successfully to {bucket_name}/{object_name}")

    except FileNotFoundError:
        logging.exception("The file was not found")

    except Exception as e:
        logging.exception(e)
