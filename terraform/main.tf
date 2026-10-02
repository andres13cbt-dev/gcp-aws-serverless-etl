# Define BigQuery, Artifact Registry, Cloud Run

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Habilitar APIs necesarias automáticamente desde Terraform
resource "google_project_service" "artifact_registry_api" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloud_run_api" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

# 2. Dataset en BigQuery (Bodega de datos)
resource "google_bigquery_dataset" "migracion_ds" {
  dataset_id  = "bodega_datos_migracion"
  location    = "US"
  description = "Dataset para almacenar data cruda y transformada para Salesforce"
}

# 3. Topic de Pub/Sub (Emisora)
resource "google_pubsub_topic" "sales_topic" {
  name = "ventas-ingestadas-topic"
}

# 4. Subscription de Pub/Sub (Oyente que activará a Job 2)
resource "google_pubsub_subscription" "sales_sub" {
  name  = "ventas-ingestadas-sub"
  topic = google_pubsub_topic.sales_topic.name

  # Retener mensajes por 1 día si Job 2 está apagado
  message_retention_duration = "86400s"
}

# 5. Artifact Registry para imágenes Docker
resource "google_artifact_registry_repository" "sales_repo" {
  depends_on    = [google_project_service.artifact_registry_api]
  location      = var.region
  repository_id = "salesforce-jobs-repo"
  format        = "DOCKER"
  description   = "Repositorio Docker para los Jobs de Migracion Salesforce"
}