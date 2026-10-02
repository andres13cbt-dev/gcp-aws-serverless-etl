import requests
import json
import os
import sys
from google.cloud import bigquery, pubsub_v1

# Importamos las configuraciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings

def run_job1():
    print("Iniciando extracción paginada desde la API...")
    
    all_data = []
    limit = 30
    skip = 0
    has_more_data = True
    
    # 1. Extracción (Simulando la API paginada)
    while has_more_data:
        paginated_url = f"https://dummyjson.com/products?limit={limit}&skip={skip}"
        print(f"Consultando: {paginated_url}")
        
        response = requests.get(paginated_url)
        if response.status_code != 200:
            raise ValueError(f"Error en API: {response.status_code} - {response.text}")
        
        data = response.json()
        items = data.get("products", [])
        
        if not items:
            break
            
        all_data.extend(items)
        skip += limit
        
        if skip >= data.get("total", 0):
            has_more_data = False

    print(f"¡Extracción completa! Registros: {len(all_data)}")

    # 2. Cargar en BigQuery
    bq_client = bigquery.Client(project=settings.GCP_PROJECT_ID)
    table_ref = f"{settings.GCP_PROJECT_ID}.{settings.BQ_DATASET}.{settings.BQ_TABLE_RAW}"

    # WRITE_TRUNCATE borra lo de ayer y pone lo de hoy. Si quieres acumular, usa WRITE_APPEND
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True
    )

    print("Cargando datos a BigQuery...")
    load_job = bq_client.load_table_from_json(all_data, table_ref, job_config=job_config)
    load_job.result() # Espera a que termine
    print(f"Los datos han sido guardados en BigQuery en la tabla: {table_ref}")

    # 3. Notificar a Pub/Sub para que despierte al Job 2
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(settings.GCP_PROJECT_ID, settings.PUBSUB_TOPIC_ID)
    
    mensaje = {"status": "SUCCESS", "records_inserted": len(all_data)}
    message_payload = json.dumps(mensaje).encode("utf-8")

    # Guardo la promesa de envío en una variable (future)
    future = publisher.publish(topic_path, message_payload)
    message_id = future.result() 
    
    print(f"Mensaje enviado a Pub/Sub con ID: {message_id}. ¡El Job 2 debería despertar pronto!")

if __name__ == "__main__":
    run_job1()