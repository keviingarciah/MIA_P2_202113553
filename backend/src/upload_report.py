# Libraries
import boto3
from dotenv import load_dotenv
import os

# Global variable
reports = []


def upload_report_file(file_path):
    global reports

    # Cargar .env
    load_dotenv("../.env")

    # Definir nombre del bucket
    bucket_name = os.getenv("BUCKET_NAME")
    # Define las credenciales directamente en el código
    aws_access_key = os.getenv("ACCES_KEY")
    aws_secret_key = os.getenv("SECRET_KEY")

    # Obtén el nombre del archivo
    file_name = os.path.basename(file_path)

    # Agregar el reporte a la lista
    reports.append(file_name)

    # Crea un cliente de S3
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )

    # Sube el archivo al bucket
    s3.upload_file(file_path, bucket_name, file_name)
