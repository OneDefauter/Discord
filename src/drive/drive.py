import os
import time
import requests
import json
import platform
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pathlib import Path

# Configurações do Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Arquivo JSON das credenciais do serviço

# Função para carregar as configurações das pastas a partir do arquivo JSON
def carregar_configuracoes_pastas():
    configuracoes_pastas = {}
    
    for file_name in os.listdir(server_drive):
        if file_name.endswith('_config.json'):
            server_id = file_name.split('_')[0]
            file_path = dir_inicial.joinpath(server_drive, file_name)
            with open(file_path) as config_file:
                config_data = json.load(config_file)
                pastas_config = config_data.get('pastas', {})
                configuracoes_pastas[server_id] = pastas_config
    return configuracoes_pastas

# Cria a instância da API do Google Drive
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

if platform.system() == 'Windows':
    server_drive = 'server\\drive'
    arquivos_procesados = 'server\\log\\arquivos_processados'
else:
    server_drive = 'server/drive'
    arquivos_procesados = 'server/log/arquivos_processados'

dir_inicial = Path(os.getcwd())

def verificar_existencia_pasta(pasta_id):
    try:
        drive_service.files().get(fileId=pasta_id).execute()
        return True  # A pasta existe
    except Exception as e:
        print(f"Erro ao verificar a existência da pasta '{pasta_id}': \n{str(e)}\n")
        return False  # A pasta não existe ou ocorreu um erro

# Função para carregar os IDs dos arquivos já processados
def carregar_arquivos_processados(server_id):
    arquivo_processado_path = dir_inicial.joinpath(arquivos_procesados, f'{server_id}_arquivos_processados.txt')
    if os.path.exists(arquivo_processado_path):
        with open(arquivo_processado_path, 'r') as file:
            arquivos_processados = {line.strip() for line in file}
    else:
        arquivos_processados = set()
    return arquivos_processados

# Função para salvar os IDs dos arquivos já processados
def salvar_arquivos_processados(arquivos_processados, server_id):
    arquivo_processado_path = dir_inicial.joinpath(arquivos_procesados, f'{server_id}_arquivos_processados.txt')
    with open(arquivo_processado_path, 'w') as file:
        file.write('\n'.join(arquivos_processados))

# Função para enviar mensagem via webhook no Discord
def enviar_mensagem_discord(name, link, created_time, last_modifying_user, pasta_id, server_id):
    atual_server_id = server_id
    for server_id, pastas_config in configuracoes_pastas.items():
        if server_id == atual_server_id:
            config = pastas_config.get(pasta_id)
            if config:
                webhook_url = config.get('webhook_url', '')
                edit_link = config.get('edit_link', '')
                project_link = config.get('project_link', '')
                raw_link = config.get('raw_link')
                comment = config.get('comment', '')
                canal_id = config.get('canal_id', '')
                avatar = config.get('avatar')
                last_modifying_user_name = last_modifying_user['displayName']
                last_modifying_user_photo = last_modifying_user.get('photoLink', '')
                cor = config.get('cor')
                if cor is not None and cor.startswith('0x'):
                    color_value = int(cor, 16)
                else:
                    color_value = cor

                raw_text = "**Link da pasta da RAW** (Não tem)" if raw_link is None else "[**Link da pasta da RAW**]({})".format(raw_link)

                print("start---------------------------------------------------------------------------------------------")
                print(comment)
                print(edit_link)
                print(project_link)
                print(raw_text)
                print(canal_id)
                print(avatar)
                print(link)
                print(name)
                print(created_time)
                print(last_modifying_user_name)
                print(last_modifying_user_photo)
                print(cor)
                print(color_value)

                data = {
                    "embeds": [
                        {
                            "title": f"**{name}**",
                            "url": link,
                            "description": f"[**Link direto**]({link})\n[**Link da pasta Editados**]({edit_link})\n[**Link da pasta do projeto**]({project_link})\n{raw_text}",
                            "timestamp": created_time,
                            "footer": {
                                "text": f"Upado por {last_modifying_user['displayName']}",
                                "icon_url": last_modifying_user.get('photoLink', '')
                            },
                            "color": color_value
                        }
                    ]
                }

                response = requests.post(webhook_url, json=data)
                if response.status_code != 204:
                    print('Ocorreu um erro ao enviar a mensagem para o Discord.')
                print("fim-----------------------------------------------------------------------------------------------\n")

# Função para monitorar a pasta no Google Drive
def monitorar_pasta(pasta_id, server_id):
    arquivos_processados = carregar_arquivos_processados(server_id)
    arquivos = []  # Definir uma lista vazia por padrão

    page_token = None
    while True:
        if verificar_existencia_pasta(pasta_id):
            response = drive_service.files().list(
                q=f"'{pasta_id}' in parents and (mimeType='application/vnd.google-apps.folder' or fileExtension='zip' or fileExtension='rar')",
                spaces='drive',
                fields='nextPageToken, files(id, name, createdTime, lastModifyingUser, webViewLink)',
                orderBy='createdTime',  # Ordenar pelos mais antigos primeiro
                pageToken=page_token
            ).execute()
            arquivos = response.get('files', [])
            arquivos.sort(key=lambda x: x['createdTime'])  # Ordenar a lista de arquivos
        else:
            print(f"A pasta {pasta_id} não existe.\n\n\n")
            break

        for arquivo in arquivos:
            if arquivo['id'] not in arquivos_processados:
                # Envia uma mensagem via webhook no Discord
                time.sleep(1)
                enviar_mensagem_discord(arquivo['name'], arquivo['webViewLink'], arquivo['createdTime'], arquivo['lastModifyingUser'], pasta_id, server_id)

                arquivos_processados.add(arquivo['id'])

        page_token = response.get('nextPageToken')
        if not page_token:
            break  # Sai do loop quando não há mais páginas de resultados

    salvar_arquivos_processados(arquivos_processados, server_id)

if __name__ == '__main__':
    while True:
        configuracoes_pastas = carregar_configuracoes_pastas()
        for server_id, pastas_config in configuracoes_pastas.items():
            print(f"Configurações do servidor {server_id}:")
            pasta_ids = list(pastas_config.keys())  # IDs das pastas que deseja monitorar no Google Drive
            for pasta_id in pasta_ids:
                # Exibir as configurações da pasta atual
                print(f"Pasta ID: {pasta_id}")
                print(f"Configurações: {json.dumps(pastas_config[pasta_id], indent=4)}\n\n\n")
                monitorar_pasta(pasta_id, server_id)
                time.sleep(1)  # Aguarda 1 segundos antes de verificar a próxima pasta    # padrão 10 segundos
