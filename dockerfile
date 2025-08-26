# Imagem base
FROM python:3.12-slim

# Define o diretório
WORKDIR /usr/src/apps/terraform_ai_agent

# Instala as dependências
RUN pip install --no-cache-dir poetry

# Copia os arquivos necessários
COPY pyproject.toml poetry.lock ./
COPY app/ ./app/

# Instala as dependências
RUN poetry install

# Expõe a porta do streamlit
EXPOSE 8501

# Comando para iniciar o streamlit
CMD ["poetry", "run", "streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
