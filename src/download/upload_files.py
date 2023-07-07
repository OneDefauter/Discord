import os, sys, time, platform, json, shutil
from concurrent import futures
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

time_sleep = 1.2

python_type = os.getenv('python_type')

if platform.system() == 'Windows':
    src_download_folder = 'src\\download'
    log_donwload = 'server\\log\\download'
else:
    src_download_folder = 'src/download'
    log_donwload = 'server/log/download'

dir_inicial = Path(os.getcwd())

# Caminho para o arquivo JSON de credenciais baixado
caminho_credenciais = "credentials.json"

# Autenticação
scopes = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(caminho_credenciais, scopes=scopes)
drive_service = build('drive', 'v3', credentials=credentials)

# Função para fazer o upload de um arquivo
def fazer_upload_arquivo(caminho_arquivo, nome_arquivo, id_pasta_destino):
    # Extrai o número da pasta do nome do arquivo
    numero_pasta = nome_arquivo.split("-")[0]
    nome_arquivo = nome_arquivo.split("-")[1]

    # Verifica se a pasta já existe no Google Drive
    lista_pasta = drive_service.files().list(
        q=f"name='{numero_pasta}' and parents='{id_pasta_destino}' and mimeType='application/vnd.google-apps.folder'",
        fields='files(id)'
    ).execute()

    if len(lista_pasta['files']) > 0:
        pasta_id = lista_pasta['files'][0]['id']
        # print(f'A pasta {numero_pasta} já existe. Utilizando a pasta existente.')
    else:
        # Cria uma nova pasta no Google Drive
        nova_pasta = drive_service.files().create(
            body={'name': numero_pasta, 'parents': [id_pasta_destino], 'mimeType': 'application/vnd.google-apps.folder'}
        ).execute()
        pasta_id = nova_pasta['id']
        print(f'Nova pasta criada: {numero_pasta}')

    # Verifica se o arquivo já foi enviado antes
    lista_arquivos = drive_service.files().list(
        q=f"parents='{pasta_id}'",
        fields='files(name)',
        pageSize=1000
    ).execute()

    nomes_arquivos = sorted([arquivo['name'] for arquivo in lista_arquivos.get('files', [])], key=lambda x: int(x.split(".")[0]))
    if nome_arquivo in nomes_arquivos:
        print(f'O arquivo {nome_arquivo} já foi enviado. Pulando...')
        return

    file_path = dir_inicial.joinpath(src_download_folder, 'upload_arquivo.py')
    # Chama o arquivo Python separado para fazer o upload do arquivo
    comando = f'{python_type} "{file_path}" "{caminho_arquivo}" "{nome_arquivo}" "{pasta_id}"'
    os.system(comando)

# Função recursiva para fazer o upload de uma pasta
def fazer_upload_pasta(pasta_local, id_pasta_destino):
    arquivos_upload = []
    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for item in os.listdir(pasta_local):
            caminho_completo = os.path.join(pasta_local, item)
            if os.path.isfile(caminho_completo):
                time.sleep(time_sleep)
                arquivo_upload = executor.submit(fazer_upload_arquivo, caminho_completo, item, id_pasta_destino)
                arquivos_upload.append(arquivo_upload)
            elif os.path.isdir(caminho_completo):
                # Verifica se a pasta já existe no Google Drive
                lista_pasta = drive_service.files().list(
                    q=f"name='{item}' and parents='{id_pasta_destino}' and mimeType='application/vnd.google-apps.folder'",
                    fields='files(id)'
                ).execute()
                if len(lista_pasta['files']) > 0:
                    nova_pasta_id = lista_pasta['files'][0]['id']
                    print(f'A pasta {item} já existe. Utilizando a pasta existente.')
                else:
                    # Cria uma nova pasta no Google Drive
                    nova_pasta = drive_service.files().create(
                        body={'name': item, 'parents': [id_pasta_destino], 'mimeType': 'application/vnd.google-apps.folder'}
                    ).execute()
                    nova_pasta_id = nova_pasta['id']
                    print(f'Nova pasta criada: {item}')

                # Chama a função recursivamente para fazer o upload da pasta interna
                fazer_upload_pasta(caminho_completo, nova_pasta_id)

    # Espera até que todos os uploads sejam concluídos
    for arquivo_upload in futures.as_completed(arquivos_upload):
        arquivo_upload.result()

# Verifica se os argumentos corretos foram fornecidos
if len(sys.argv) != 3:
    print("Uso: python upload_files.py pasta_local id_pasta_destino")
    sys.exit(1)

# Obtém os argumentos da linha de comando
pasta_local = sys.argv[1]
id_pasta_destino = sys.argv[2]

# Lê o valor max_workers do arquivo download.json
max_workers = 1
file_path = dir_inicial.joinpath(log_donwload, 'download.json')
with open(file_path, 'r') as json_file:
    config = json.load(json_file)
    if 'max_workers' in config:
        max_workers = int(config['max_workers'])

# Chama a função para fazer o upload da pasta
fazer_upload_pasta(pasta_local, id_pasta_destino)
