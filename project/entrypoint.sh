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

# Inicia a aplicação
echo "Waiting for start app..."
uvicorn --host 0.0.0.0 --port 3050 project.app:app --reload
