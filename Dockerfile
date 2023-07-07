# Use uma imagem base do Python
FROM python:3

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /home/ubuntu/Discord

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o diretório de trabalho
COPY . .

# Defina o comando padrão para ser executado quando o contêiner for iniciado
CMD ["python3", "main.py"]
