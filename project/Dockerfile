FROM python:3.13-alpine

ARG USER_ID=1000
ARG GROUP_ID=1000

# Atualizar os índices de pacotes e instalar dependências de compilação
RUN apk update && \
    apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 bash

# Instalar pip e suas dependências
RUN pip3 install --upgrade pip setuptools wheel

WORKDIR /srv/

# Copiar os arquivos necessários, incluindo o arquivo de requisitos
COPY ./requirements.txt /srv/requirements.txt

# Instalar as dependências do Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Instalar Alembic separadamente (se necessário)
RUN pip install --no-cache-dir alembic

# Copiar todos os arquivos do projeto
COPY . /srv/

# Adicionar grupo e usuário com UID e GID personalizados
RUN addgroup -g $GROUP_ID usergroup && \
    adduser -D -u $USER_ID -G usergroup docker

# Ajustar permissões para o usuário docker
RUN chown -R docker:usergroup /srv/ && \
    chmod -R 755 /srv/

# Trocar para o usuário docker
USER docker

# Expor a porta definida pelo argumento
EXPOSE 3030

# Comando para rodar a aplicação
CMD ["uvicorn", "project.app:app", "--host", "0.0.0.0", "--port", "3030", "--reload"]
