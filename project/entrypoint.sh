#!/bin/sh

# Executa as migrações do banco de dados
alembic upgrade head

# Inicia a aplicação
uvicorn --host 0.0.0.0 --port 3030 project.app:app
