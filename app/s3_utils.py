import boto3
import os
from botocore.exceptions import NoCredentialsError

# Инициализация клиента MinIO
def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=os.getenv('MINIO_ENDPOINT'),
        aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('MINIO_SECRET_KEY'),
    )

# Загрузка файла в S3
def upload_file_to_s3(file_path, bucket_name=None, object_name=None):
    client = get_s3_client()
    if bucket_name is None:
        bucket_name = os.getenv("MINIO_BUCKET_NAME")
    if object_name is None:
        object_name = file_path.split("/")[-1]
    try:
        client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to bucket {bucket_name} as {object_name}.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Скачивание файла из S3
def download_file_from_s3(bucket_name=None, object_name=None, output_path=None):
    client = get_s3_client()
    if bucket_name is None:
        bucket_name = os.getenv("MINIO_BUCKET_NAME")
    if output_path is None:
        output_path = object_name
    try:
        client.download_file(bucket_name, object_name, output_path)
        print(f"File {object_name} downloaded from bucket {bucket_name} to {output_path}.")
    except Exception as e:
        print(f"Error downloading file: {e}")