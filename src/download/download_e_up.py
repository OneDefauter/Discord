import json, subprocess, datetime, re, discord, discord.ext, os, signal, asyncio, configparser, shutil, sys, platform
from discord.ext import commands
from discord import app_commands, Client
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from urllib.parse import urlparse, parse_qs
from pathlib import Path

load_dotenv()

python_type = os.getenv('python_type')

link = sys.argv[1]
pasta_link = sys.argv[2]
nova_pasta_id = sys.argv[3]

if platform.system() == 'Windows':
    src_download_folder = 'src\\download'
else:
    src_download_folder = 'src/download'

dir_inicial = Path(os.getcwd())

def verificar_link_e_baixar2(link, pasta_link, nova_pasta_id):
    try:
        # Criar a pasta para os arquivos
        pasta_obras = "Obras"
        pasta_destino = os.path.join(pasta_obras, pasta_link)
        os.makedirs(pasta_destino, exist_ok=True)

        # Executar o comando gallery-dl com o diretório de destino especificado
        comando = f'gallery-dl "{link}" -D {pasta_destino}'
        subprocess.run(comando, shell=True, check=True)

        # Mover as imagens para as pastas dos capítulos
        # mover_imagens_para_capitulos(pasta_destino)

        processes = []
        file_path = dir_inicial.joinpath(src_download_folder, 'main_.py')
        comando = f'{python_type} "{file_path}" "{pasta_link}" "{nova_pasta_id}"'
        process = subprocess.Popen(comando, shell=True)
        processes.append(process)

        # Enviar a resposta final
        print("Ok!")
    except subprocess.CalledProcessError:
        print("Ocorreu um erro.")

def mover_imagens_para_capitulos(pasta_destino):
    # Obter a lista de arquivos baixados
    arquivos = os.listdir(pasta_destino)
    arquivos.sort()

    # Expressão regular para extrair o número do capítulo do nome do arquivo
    padrao = r"(\d+)-\d+\.(jpg|png)"  # <capítulo>-<página>.<extensão>

    # Mover cada arquivo para a pasta do respectivo capítulo
    for arquivo in arquivos:
        if arquivo.endswith(".jpg") or arquivo.endswith(".png"):
            # Extrair o número do capítulo do nome do arquivo
            correspondencia = re.match(padrao, arquivo)
            if correspondencia:
                numero_capitulo = correspondencia.group(1)
                pasta_capitulo = os.path.join(pasta_destino, numero_capitulo)
                os.makedirs(pasta_capitulo, exist_ok=True)
                caminho_arquivo_origem = os.path.join(pasta_destino, arquivo)
                caminho_arquivo_destino = os.path.join(pasta_capitulo, arquivo)
                if os.path.exists(caminho_arquivo_destino):
                    os.remove(caminho_arquivo_destino)
                os.rename(caminho_arquivo_origem, caminho_arquivo_destino)

verificar_link_e_baixar2(link, pasta_link, nova_pasta_id)