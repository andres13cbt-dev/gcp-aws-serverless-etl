# Serverless ETL Pipeline: GCP & AWS S3 Integration 

Este proyecto es un pipeline de datos Serverless (ETL) automatizado, diseñado para extraer datos de una API externa, almacenarlos en una bodega de datos (Data Warehouse), transformarlos y exportarlos a un Data Lake cross-cloud.

La infraestructura está 100% gestionada como código (IaC) y el procesamiento está contenedorizado, optimizado para ejecutarse en la capa gratuita de la nube.

## Arquitectura del Proyecto

El flujo se divide en dos trabajos asíncronos desacoplados mediante un bus de mensajería:

1. **Job 1 (Ingesta):** Extrae datos paginados de una API REST (DummyJSON), procesa la carga completa y la inserta en **Google BigQuery** (Raw Data). Al finalizar, publica un evento de éxito en **Google Pub/Sub**.
2. **Job 2 (Exportación):** Lee desde BigQuery utilizando consultas SQL separadas del código, transforma los datos (ej. filtrado por reglas de negocio) y los exporta en formato CSV a un bucket de **AWS S3**.

## Stack Tecnológico

* **Lenguaje:** Python 3.11
* **Contenedores:** Docker, Artifact Registry
* **Cómputo:** Google Cloud Run Jobs
* **Orquestación:** Cloud Scheduler, Eventarc (Pub/Sub)
* **Almacenamiento:** BigQuery (GCP), Amazon S3 (AWS)
* **Infraestructura como Código (IaC):** Terraform

## Estructura del Repositorio

```text
├── config/
│   └── settings.py          # Gestión centralizada de variables de entorno
├── sql/
│   └── transform_export_s3.sql # Lógica de transformación separada
├── src/
│   ├── job1_ingest.py       # Lógica de extracción e ingesta a BQ
│   └── job2_export.py       # Lógica de transformación y carga a AWS
├── terraform/
│   └── main.tf              # Definición de infraestructura GCP
├── .env.example             # Plantilla de variables requeridas
├── .dockerignore
├── .gitignore
├── Dockerfile               # Receta de empaquetado unificado
├── requirements.txt         # Dependencias de Python
└── README.md
```
---

**Despliegue y Ejecución Local**

1. Requisitos Previos

Terraform instalado.
Docker Desktop / Engine instalado.
Cuentas activas en Google Cloud Platform (GCP) y AWS.
gcloud CLI instalado y autenticado (gcloud auth application-default login).

2. Configurar Variables de Entorno

Clona el repositorio y crea un archivo .env basado en .env.example:
Bash
GCP_PROJECT_ID=tu-proyecto-gcp
BQ_DATASET=bodega_datos_migracion
BQ_TABLE_RAW=raw_ventas_svn
PUBSUB_TOPIC_ID=ventas-ingestadas-topic
AWS_ACCESS_KEY_ID=tu_aws_key
AWS_SECRET_ACCESS_KEY=tu_aws_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=tu-bucket-s3

3. Desplegar Infraestructura (Terraform)

Bash
cd terraform
terraform init
terraform apply

4. Ejecución Local (Opcional)

Puedes probar los scripts de Python directamente en tu entorno virtual:
Bash
python src/job1_ingest.py
python src/job2_export.py

5. Despliegue en Cloud Run

Construye y sube la imagen al registro de contenedores:
Bash
docker build -t us-east4-docker.pkg.dev/TU_PROYECTO/salesforce-jobs-repo/migracion-job:v1 .
docker push us-east4-docker.pkg.dev/TU_PROYECTO/salesforce-jobs-repo/migracion-job:v1
Luego, configura los Cloud Run Jobs inyectando la variable JOB_TO_RUN=job1 o JOB_TO_RUN=job2 según corresponda.

