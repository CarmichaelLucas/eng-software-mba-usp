#!/bin/sh

if [ "$WAIT_FOR_DB" = 1 ]; then
  echo "Waiting for database..."

  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.1
  done

  echo "database started"
fi

# Executa as migrações do banco de dados
echo "Waiting for migrations..."
alembic upgrade head

export OTEL_SERVICE_NAME="todo"
export OTEL_EXPORTER_OTLP_ENDPOINT="otel:4317"
export OTEL_EXPORTER_OTLP_INSECURE=true
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLE=true
export OTEL_TRACES_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp

# Inicia a aplicação
echo "Waiting for start app..."
opentelemetry-bootstrap -a install
opentelemetry-instrument uvicorn --host 0.0.0.0 --port 3030 todo.app:app --reload
