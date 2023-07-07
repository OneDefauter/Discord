import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Caminho para o arquivo JSON de credenciais baixado
caminho_credenciais = "credentials.json"

# Autenticação
scopes = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(caminho_credenciais, scopes=scopes)
drive_service = build('drive', 'v3', credentials=credentials)

# Obtém os argumentos da linha de comando
caminho_arquivo = sys.argv[1]
nome_arquivo = sys.argv[2]
id_pasta_destino = sys.argv[3]

# Faz o upload do arquivo
media = MediaFileUpload(caminho_arquivo)
arquivo = drive_service.files().create(
    media_body=media,
    body={'name': nome_arquivo, 'parents': [id_pasta_destino]}
).execute()
print(f'Upload concluído: {nome_arquivo}')
