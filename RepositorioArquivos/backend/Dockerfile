# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos para o container
COPY . /app

# Instale as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt --upgrade

# Exponha a porta 5000
EXPOSE 5000

# Define o PYTHONPATH para incluir o diretório /app
ENV PYTHONPATH=/app

# Comando para iniciar o aplicativo
CMD ["python", "-m", "app.main"]