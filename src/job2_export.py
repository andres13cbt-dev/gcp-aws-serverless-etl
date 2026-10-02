import os
import sys
import boto3
from google.cloud import bigquery

# Importamos las configuraciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings

def run_job2():
    print("Iniciando lectura desde BigQuery y envío a AWS S3...")
    
    bq_client = bigquery.Client(project=settings.GCP_PROJECT_ID)
    
    # Cliente de AWS S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    # 1. Leer el archivo SQL
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'venta_directa.sql')
    with open(sql_path, 'r') as file:
        query_template = file.read()
    
    # 2. Inyectar variables al SQL
    query = query_template.format(
        PROJECT_ID=settings.GCP_PROJECT_ID,
        DATASET=settings.BQ_DATASET,
        TABLE_RAW=settings.BQ_TABLE_RAW
    )

    # 3. Ejecutar consulta en BigQuery y convertir a DataFrame
    print("Ejecutando SQL en BigQuery...")
    df = bq_client.query(query).to_dataframe()
    print(f"Registros procesados por SQL: {len(df)}")

    # 4. Convertir a CSV (en memoria, sin guardar en el disco duro del contenedor)
    csv_buffer = df.to_csv(index=False).encode('utf-8')
    s3_key = "salesforce_extracts/venta_directa_data.csv"

    # 5. Subir a AWS S3
    print("Subiendo archivo a AWS S3...")
    s3_client.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key,
        Body=csv_buffer
    )
    
    print(f"Archivo disponible en s3://{settings.S3_BUCKET_NAME}/{s3_key}")

if __name__ == "__main__":
    run_job2()