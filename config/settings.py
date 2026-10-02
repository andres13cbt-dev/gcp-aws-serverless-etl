import os
from dotenv import load_dotenv

load_dotenv()

# GCP Config
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "sim-migracion")
BQ_DATASET = os.getenv("BQ_DATASET", "bodega_datos_migracion")
BQ_TABLE_RAW = os.getenv("BQ_TABLE_RAW", "raw_ventas_svn")
PUBSUB_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "ventas-ingestadas-topic")

# AWS Config
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "MOCK_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "MOCK_SECRET")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "amzn-s3-bucket-sim-migracion ")

# Endpoint Simulado (Reemplaza la BD SVN Java)
MOCK_ENDPOINT_URL = "https://dummyjson.com/carts"