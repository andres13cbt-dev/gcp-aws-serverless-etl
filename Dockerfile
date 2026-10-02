FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Por defecto ejecuta Job 1, pero se puede sobrescribir
ENV JOB_TO_RUN="job1"
CMD ["sh", "-c", "if [ \"$JOB_TO_RUN\" = \"job1\" ]; then python src/job1_ingest.py; else python src/job2_export.py; fi"]

# CMD ["python", "src/job1_ingest_local.py"] para ejecutar el job1 localmente