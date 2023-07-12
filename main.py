import importlib, os, subprocess

if os.name == 'nt':  # Verifica se o sistema é Windows
    subprocess.check_call(['python.exe -m pip install --upgrade pip'])

biblioteca = ['requests', 'python-dotenv', 'discord', 'pytz', 'google-auth', 'google-api-python-client', 'google-auth-oauthlib', 'pillow', 'psutil', 'gallery-dl', 'beautifulsoup4']

def verificar_e_instalar_modulo(module_name):
    try:
        importlib.import_module(module_name)
        print(f"O módulo {module_name} já está instalado.\n")
    except ImportError:
        print(f"O módulo {module_name} não está instalado. Instalando...")
        subprocess.check_call(['pip', 'install', module_name])
        print(f"O módulo {module_name} foi instalado com sucesso.\n")

# Exemplo de uso
for a in biblioteca:
    verificar_e_instalar_modulo(a)

def limpar_console():
    if os.name == 'nt':  # Verifica se o sistema é Windows
        os.system('cls')  # Comando para limpar o console no Windows
    else:
        os.system('clear')  # Comando para limpar o console em sistemas Unix-like

limpar_console()





import json, datetime, re, urllib.request, requests, discord, discord.ext, shutil, asyncio, sys, pytz, platform, io, time
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List
from PIL import Image

start_time = datetime.datetime.now()

if platform.system() == 'Windows':
    server_drive = 'server\\drive'
    arquivos_procesados = 'server\\log\\arquivos_processados'
    src_folder = 'src'
    src_download_folder = 'src\\download'
    src_drive_folder = 'src\\drive'
    log_download = 'server\\log\\download'
    log_comandos = 'server\\log\\comandos'
else:
    server_drive = 'server/drive'
    arquivos_procesados = 'server/log/arquivos_processados'
    src_folder = 'src'
    src_download_folder = 'src/download'
    src_drive_folder = 'src/drive'
    log_download = 'server/log/download'
    log_comandos = 'server/log/comandos'

dir_inicial = Path(os.getcwd())

if os.path.exists("update.py"):
    os.remove("update.py")

load_dotenv()

bot_token1 = os.getenv('BOT_TOKEN1')
bot_token2 = os.getenv('BOT_TOKEN2')
python_type = os.getenv('python_type')

intents = discord.Intents.all()
client1 = discord.Client(intents=intents)
tree1 = discord.app_commands.CommandTree(client1)
client2 = discord.Client(intents=intents)
tree2 = discord.app_commands.CommandTree(client2)

# Função para obter a versão de um pacote usando o comando "pip show"
def get_package_version(package_name):
    try:
        result = subprocess.check_output(['pip', 'show', package_name]).decode('utf-8')
        for line in result.split('\n'):
            if line.startswith('Version:'):
                return line.split(': ')[1].strip()
    except subprocess.CalledProcessError:
        return None

monitoramento_ativo = False
main_version = "3.1"
bot_version = discord.__version__
google_api_core_version = get_package_version('google-api-core')
google_api_python_client_version = get_package_version('google-api-python-client')
google_auth_version = get_package_version('google-auth')
GITHUB_REPO = "https://api.github.com/repos/OneDefauter/Discord"

# Configurações do Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Arquivo JSON das credenciais do serviço

update_url = None
drive_url = None
main__url = None
upload_arquivo_url = None
upload_files_url = None
download_e_up_url = None
latest_version = None

def get_uris():
    global update_url
    global main__url
    global upload_arquivo_url
    global upload_files_url
    global download_e_up_url
    global latest_version
    response = requests.get(f"{GITHUB_REPO}/releases/latest")
    response.raise_for_status()
    latest_version = response.json()["tag_name"]
    release_url = response.json()["url"]
    release_response = requests.get(release_url)
    release_response.raise_for_status()
    assets = release_response.json()["assets"]
    for asset in assets:
        if asset["name"] == "update.py":
            update_url = asset["browser_download_url"]
        if asset["name"] == "main_.py":
            main__url = asset["browser_download_url"]
        if asset["name"] == "upload_arquivo.py":
            upload_arquivo_url = asset["browser_download_url"]
        if asset["name"] == "upload_files.py":
            upload_files_url = asset["browser_download_url"]
        if asset["name"] == "download_e_up.py":
            download_e_up_url = asset["browser_download_url"]

def start_files():
    download = dir_inicial.joinpath(src_download_folder)
    
    if not os.path.exists(download):
        os.makedirs(download)
    main__path = os.path.join(download, 'main_.py')
    upload_arquivo_path = os.path.join(download, 'upload_arquivo.py')
    upload_files_path = os.path.join(download, 'upload_files.py')
    download_e_up_path = os.path.join(download, 'download_e_up.py')

    if not os.path.exists(main__path):
        print(main__path)
        urllib.request.urlretrieve(main__url, main__path)
    if not os.path.exists(upload_arquivo_path):
        print(upload_arquivo_path)
        urllib.request.urlretrieve(upload_arquivo_url, upload_arquivo_path)
    if not os.path.exists(upload_files_path):
        print(upload_files_path)
        urllib.request.urlretrieve(upload_files_url, upload_files_path)
    if not os.path.exists(download_e_up_path):
        print(download_e_up_path)
        urllib.request.urlretrieve(download_e_up_url, download_e_up_path)

def start_folders():
    drive_folder = dir_inicial.joinpath(server_drive)
    arquivos_procesados_folder = dir_inicial.joinpath(arquivos_procesados)
    log_download_folder = dir_inicial.joinpath(log_download)
    log_comandos_folder = dir_inicial.joinpath(log_comandos)
    if not os.path.exists(drive_folder):
        os.makedirs(drive_folder)
    if not os.path.exists(arquivos_procesados_folder):
        os.makedirs(arquivos_procesados_folder)
    if not os.path.exists(log_download_folder):
        os.makedirs(log_download_folder)
    if not os.path.exists(log_comandos_folder):
        os.makedirs(log_comandos_folder)

 
get_uris()
start_files()
start_folders()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot1 = loop.create_task(client1.start(bot_token1, reconnect = True))
bot2 = loop.create_task(client2.start(bot_token2, reconnect = True))

@client1.event
async def on_ready():
    await client1.change_presence(status=discord.Status.online)
    print('-------------------------------------------')
    print('Main')
    print(f'Bot conectado como {client1.user.name}')
    print('ID do Bot:', client1.user.id)
    print(f'Versão: {main_version}')
    print("Online: ✅")
    print('-------------------------------------------\n')
    await tree1.sync()
    if os.path.exists("last_channel.txt"):
        with open("last_channel.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                server_id = lines[0].strip().split(":")[-1].strip()
                channel_id = lines[1].strip().split(":")[-1].strip()

        if server_id and channel_id:
            # Enviar uma mensagem no canal especificado
            guild = client1.get_guild(int(server_id))
            channel = guild.get_channel(int(channel_id))
        
            if channel:
                await channel.send("O bot foi atualizado.")
                os.remove("last_channel.txt")
            else:
                print("Canal não encontrado.")
        else:
            print("ID do servidor e/ou ID do canal não encontrados.")

@client2.event
async def on_ready():
    await client2.change_presence(status=discord.Status.online)
    await client2.change_presence(activity=discord.Game(name="Drive: Desligado"))
    print('-------------------------------------------')
    print('Bot')
    print(f'Bot conectado como {client2.user.name}')
    print('ID do Bot:', client2.user.id)
    print(f'Versão: {bot_version}')
    print("Online: ✅")
    print('-------------------------------------------\n')
    await tree2.sync()

@client1.event
async def on_connect():
    print('Bot conectado ao servidor Discord\n')



def registrar_comando(nome_comando, autor, server_id):
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mensagem = f"{data_hora} - Comando '{nome_comando}' usado por {autor}"
    file_path1 = dir_inicial.joinpath(log_comandos)
    
    if not os.path.exists(file_path1):
        os.makedirs(file_path1)
    file_path = os.path.join(file_path1, f'{server_id}_comandos.log')
    with open(file_path, 'a') as arquivo_log:
        arquivo_log.write(mensagem + '\n')

    try:
        with open("version.log", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return main_version

def verificar_atualizacao():
    try:
        with urllib.request.urlopen("https://github.com/OneDefauter/Menu_/releases/download/ChangeLog/version.txt") as url:
            data = url.read().decode()
            config = json.loads(data)
            version = config.get("Version_Menu")
            return version
    except Exception as e:
        print(f"Ocorreu um erro ao verificar a atualização: {str(e)}")
        return None

# Carrega as configurações do arquivo config.json
def carregar_configuracoes(server_id):
    file_path = dir_inicial.joinpath(server_drive, f'{server_id}_config.json')

    if os.path.exists(file_path):
        with open(file_path) as config_file:
            config_data = json.load(config_file)
            return config_data.get('pastas', {})
    else:
        return {}

# Salva as configurações no arquivo config.json
def salvar_configuracoes(configuracoes, server_id):
    file_path = dir_inicial.joinpath(server_drive, f'{server_id}_config.json')
    with open(file_path, 'w') as config_file:
        json.dump({'pastas': configuracoes}, config_file, indent=4)

async def verificar_link_e_baixar(interaction, link, link_sem_parametros):
    # Verificar se o link é permitido
    links_permitidos = ["https://comic.naver.com/webtoon/","https://www.webtoons.com/en/"]
    if not any(link.startswith(permitido) for permitido in links_permitidos):
        await interaction.response.send_message("Desculpe, o link fornecido não é permitido.")
        return
    
    # await interaction.response.send_message("Iniciando...")
    await interaction.response.defer()
    if any(link.startswith(permitido) for permitido in links_permitidos):
        image_url = get_url_image(link_sem_parametros)
        get_name = get_url_name(link_sem_parametros)

    try:
        if link.startswith("https://comic.naver.com/webtoon/"):
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)
            pasta_link = query_params.get('titleId', [''])[0]
        if link.startswith("https://www.webtoons.com/en/"):
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)
            pasta_link = query_params.get('title_no', [''])[0]
        
        # Autenticação
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=scopes)
        drive_service = build('drive', 'v3', credentials=credentials)

        lista_pasta = drive_service.files().list(
            q=f"name='{pasta_link}' and parents='1af9Dg2ugnacDtj17gnTGhn-yi8Z9tuLc' and mimeType='application/vnd.google-apps.folder'",
            fields='files(id)'
        ).execute()

        if len(lista_pasta['files']) > 0:
            nova_pasta_id = lista_pasta['files'][0]['id']
            print(f'A pasta {pasta_link} já existe. Utilizando a pasta existente.')
        else:
            # Cria uma nova pasta no Google Drive
            nova_pasta = drive_service.files().create(
                body={'name': pasta_link, 'parents': ['1af9Dg2ugnacDtj17gnTGhn-yi8Z9tuLc'], 'mimeType': 'application/vnd.google-apps.folder'}
            ).execute()
            nova_pasta_id = nova_pasta['id']
            print(f'Nova pasta criada: {pasta_link}')

        

        processes = []
        file_path = dir_inicial.joinpath(src_download_folder, 'download_e_up.py')
        comando = f'{python_type} "{file_path}" "{link}" "{pasta_link}" "{nova_pasta_id}"'
        process = subprocess.Popen(comando, shell=True)
        processes.append(process)

        embed = discord.Embed(title=f"{get_name} ({pasta_link})",url=f"{link_sem_parametros}",description="**Os arquivos serão enviados neste** [**link aqui.**](https://drive.google.com/drive/folders/" + nova_pasta_id + "?usp=drive_link)",color=discord.Color.green())
        embed.add_field(name="**Link usado:**", value=f"**{link}**",inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_image(url=f"{image_url}")
        embed.set_footer(text='\u200b',icon_url="https://cdn.discordapp.com/app-icons/1015651861069582356/548d572985e177face2f967b05bcc3df.png?size=256")
        await interaction.followup.send(embed=embed)
    except subprocess.CalledProcessError:
        print("Ocorreu um erro.")

def atualizar_valor_upload_config(upload):
    file_path = dir_inicial.joinpath(log_download, 'download.json')
    if not os.path.exists(file_path):
        # Se o arquivo não existir, crie um arquivo vazio
        with open(file_path, 'w') as arquivo:
            arquivo.write("{}")

    with open(file_path, 'r') as config_file:
        config = json.load(config_file)

    config['max_workers'] = upload

    with open(file_path, 'w') as config_file:
        json.dump(config, config_file)

def get_url_image(link_sem_parametros):
    # Faz a requisição HTTP
    response = requests.get(link_sem_parametros)

    # Obtém o conteúdo HTML da página
    html = response.content

    # Parseia o HTML usando o BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontra a tag <meta> com o atributo 'property' igual a 'og:image'
    meta_tag = soup.find('meta', attrs={'property': 'og:image'})

    # Obtém o valor do atributo 'content' da tag encontrada
    if meta_tag:
        image_url = meta_tag.get('content')
        return image_url

def get_url_name(link_sem_parametros):
    # Faz a requisição HTTP
    response = requests.get(link_sem_parametros)

    # Obtém o conteúdo HTML da página
    html = response.content

    # Parseia o HTML usando o BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontra a tag <meta> com o atributo 'property' igual a 'og:image'
    meta_tag = soup.find('meta', attrs={'property': 'og:title'})

    # Obtém o valor do atributo 'content' da tag encontrada
    if meta_tag:
        get_name = meta_tag.get('content')
        return get_name

def remove_parametro_no(link):
    # parse o URL
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    path_parts = parsed_url.path.split('/')
    
    # Se for um link naver, remove o parâmetro 'no' (se ele existir)
    if "comic.naver.com" in link:
        if 'no' in query_params:
            del query_params['no']
    
    # Se for um link webtoon, reescreve o URL
    elif "webtoons.com" in link:
        # O path_parts tem o formato ['', 'en', 'genre', 'title', 'action', ...]
        # Nós queremos reescrever para ['', 'en', 'genre', 'title', 'list']
        if len(path_parts) > 4:
            path_parts = path_parts[:4] + ['list']
            parsed_url = parsed_url._replace(path='/'.join(path_parts))
         
        # Remover o parâmetro 'episode_no' da query string (se ele existir)
        if 'episode_no' in query_params:
            del query_params['episode_no']

    # Atualizar a query string sem o parâmetro 'no' ou 'episode_no'
    parsed_url = parsed_url._replace(query=urlencode(query_params, doseq=True))

    # Reconstruir o URL sem o parâmetro 'no' ou 'episode_no'
    link_sem_parametros = urlunparse(parsed_url)
    return link_sem_parametros

def handle_signal():
    loop.stop()
    loop.close()
    sys.exit()

def monitoring_stop():
    global discord_process
    if discord_process is None:
        return
    discord_process.terminate()
    discord_process.wait()
    discord_process = None

def get_all_colors():
    colors_database = {
        'Amarelo': '#FFFF00',
        'Amarelo Claro': '#FFFFE0',
        'Amêndoa Esbranquiçada': '#FFEBCD',
        'Ameixa': '#DDA0DD',
        'Aqua': '#00FFFF',
        'Azul': '#0000FF',
        'Azul Ardósia': '#6A5ACD',
        'Azul Ardósia Claro': '#B0C4DE',
        'Azul Ardósia Escuro': '#483D8B',
        'Azul Ardósia Médio': '#7B68EE',
        'Azul Aço': '#4682B4',
        'Azul Aço Claro': '#B0E0E6',
        'Azul Cadete': '#5F9EA0',
        'Azul Céu': '#87CEEB',
        'Azul Céu Claro': '#87CEFA',
        'Azul Céu Profundo': '#0000FF',
        'Azul Dodger': '#1E90FF',
        'Azul-marinho': '#000080',
        'Azul Meia-Noite': '#191970',
        'Azul Pó': '#AFEEEE',
        'Azul Royal': '#4169E1',
        'Azul Violeta': '#8A2BE2',
        'Azul-piscina': '#E0FFFF',
        'Azul Centáurea': '#6495ED',
        'Bisque': '#FFE4C4',
        'Branco': '#FFFFFF',
        'Branco Antigo': '#FAEBD7',
        'Branco Fantasma': '#F8F8FF',
        'Branco Floral': '#FFF9E6',
        'Branco Navajo': '#FFDEAD',
        'Bronzeado': '#D2B48C',
        'Caqui': '#F0E68C',
        'Caqui Escuro': '#BDB76B',
        'Cardo': '#D8BFD8',
        'Carmesim': '#DC143C',
        'Chiffon de Limão': '#FFFACD',
        'Chocolate': '#D2691E',
        'Ciano': '#00FFFF',
        'Ciano Claro': '#E0FFFF',
        'Ciano Escuro': '#008B8B',
        'Cinza': '#808080',
        'Cinza Ardósia': '#708090',
        'Cinza Ardósia Claro': '#B0C4DE',
        'Cinza Ardósia Escuro': '#2F4F4F',
        'Cinza Claro': '#D3D3D3',
        'Cinza Escuro': '#A9A9A9',
        'Cinza Fosco': '#696969',
        'Concha do Mar': '#FFF5EE',
        'Coral': '#FF7F50',
        'Coral Claro': '#F08080',
        'Creme de Menta': '#98FB98',
        'Fumaça Branca': '#F5F5F5',
        'Fúcsia': '#FF00FF',
        'Gainsboro': '#DCDCDC',
        'Laranja': '#FFA500',
        'Laranja Escuro': '#FF8C00',
        'Lavanda': '#E6E6FA',
        'Lima': '#00FF00',
        'Linho': '#FAF0E6',
        'Madeira Burly': '#DEB887',
        'Magenta': '#FF00FF',
        'Magenta Escuro': '#8B008B',
        'Marfim': '#FFFFF0',
        'Marrom': '#A52A2A',
        'Marrom Arenoso': '#C0B090',
        'Marrom Rosado': '#BC8F8F',
        'Marrom Sela': '#8B4513',
        'Mel-de-orvalho': '#F5FFFA',
        'Neve': '#FFF9F0',
        'Oliva': '#808000',
        'Orquídea': '#DA70D6',
        'Orquídea Escuro': '#9932CC',
        'Orquídea Médio': '#BA55D3',
        'Ouro Velho': '#DAA520',
        'Ouro Velho Escuro': '#B8860B',
        'Ouro Velho Pálido': '#EEDD82',
        'Peru': '#CD853F',
        'Puff de Pêssego': '#FFDAB9',
        'Prateado': '#C0C0C0',
        'Preto': '#000000',
        'Renda Antiga': '#A09E9C',
        'Rosa': '#FF69B4',
        'Rosa Claro': '#FFB6C1',
        'Rosa Empoeirado': '#FFE4E1',
        'Rosa Profundo': '#FF1493',
        'Rubor de Lavanda': '#FFAEB9',
        'Roxo': '#800080',
        'Roxo Médio': '#9370DB',
        'Salmão': '#FA8072',
        'Salmão Claro': '#FDAB9F',
        'Salmão Escuro': '#E9967A',
        'Sienna': '#A0522D',
        'Tomate': '#FF6347',
        'Trigo': '#D2B48C',
        'Turquesa': '#40E0D0',
        'Turquesa Escuro': '#00CED1',
        'Turquesa Médio': '#48D1CC',
        'Turquesa Pálido': '#AFEEEE',
        'Verde': '#008000',
        'Verde-amarelado': '#9ACD32',
        'Verde-amarelo': '#ADFF2F',
        'Verde-cartucho': '#808000',
        'Verde Claro': '#90EE90',
        'Verde Escuro': '#006400',
        'Verde Floresta': '#228B22',
        'Verde Grama': '#7CFC00',
        'Verde Marinho': '#2E8B57',
        'Verde Marinho Claro': '#20B2AA',
        'Verde Marinho Escuro': '#8DEEEE',
        'Verde Marinho Médio': '#3D59AB',
        'Verde Oliva': '#6B8E23',
        'Verde Oliva Escuro': '#556B2F',
        'Verde Pálido': '#98FB98',
        'Verde Primavera': '#00FF7F',
        'Verde Primavera Médio': '#00FA9A',
        'Verde-lima': '#32CD32',
        'Vermelho': '#FF0000',
        'Vermelho Alaranjado': '#FF4500',
        'Vermelho Escuro': '#8B0000',
        'Vermelho Indiano': '#CD5C5C',
        'Vermelho Violeta': '#EE82EE',
        'Vermelho Violeta Médio': '#C71585',
        'Whip de Papaia': '#FFEFD5',
        'Azul Celeste': '#B2FFFF',
        'Azul Claro': '#ADD8E6',
        'Azul Escuro': '#00008B',
        'Azul Marinho Médio': '#000080',
        'Azul Marinho-claro': '#1974D2',
        'Azul Meia-Noite Claro': '#191970',
        'Azul Meia-Noite Escuro': '#000033',
        'Azul Meia-Noite Médio': '#191970',
        'Azul Meia-Noite-claro': '#2B65EC',
        'Azul Meia-Noite-escuro': '#003366',
        'Azul Médio': '#0000CD',
        'Azul Pálido': '#AFEEEE',
        'Azul-claro': '#87CEEB',
        'Azul-céu': '#87CEEB',
        'Azul-céu Claro': '#87CEFA',
        'Azul-céu Escuro': '#00BFFF',
        'Azul-céu Médio': '#6CA6CD',
        'Azul-dodger Claro': '#1E90FF',
        'Azul-dodger Escuro': '#0000C8',
        'Azul-dodger Médio': '#0000CD',
        'Azul-marinho Claro': '#000080',
        'Azul-marinho Escuro': '#000033',
        'Azul-marinho Médio': '#0000CD',
        'Azul-marinho-claro': '#4169E1',
        'Azul-marinho-escuro': '#00008B',
        'Azul-piscina Claro': '#ADD8E6',
        'Azul-piscina Escuro': '#66CDAA',
        'Azul-piscina Médio': '#00BFFF',
        'Cinza-claro': '#D3D3D3',
        'Cinza-escuro': '#A9A9A9',
        'Cinza-fosco': '#696969',
        'Coral-claro': '#F08080',
        'Coral-escuro': '#FF4500',
        'Creme-de-menta Claro': '#98FB98',
        'Creme-de-menta Escuro': '#90EE90',
        'Creme-de-menta Médio': '#00FA9A',
        'Fúcsia Claro': '#FF00FF',
        'Fúcsia Escuro': '#800080',
        'Fúcsia Médio': '#FF00FF',
        'Laranja Claro': '#FFA500',
        'Laranja Escuro': '#FF8C00',
        'Laranja-claro': '#FF7F50',
        'Laranja-escuro': '#FF4500',
        'Lavanda Claro': '#E6E6FA',
        'Lavanda Escuro': '#9932CC',
        'Lavanda Médio': '#BA55D3',
        'Lavanda-claro': '#FFF0F5',
        'Lavanda-escuro': '#8B4789',
        'Lima Claro': '#00FF00',
        'Lima Escuro': '#008000',
        'Lima Médio': '#32CD32',
        'Marfim-claro': '#FFFFF0',
        'Marfim-escuro': '#FFFFE0',
        'Marrom-claro': '#D2B48C',
        'Marrom-escuro': '#8B4513',
        'Marrom-rosado': '#BC8F8F',
        'Marrom-sela': '#8B4513',
        'Mel-de-orvalho-claro': '#F5FFFA',
        'Mel-de-orvalho-escuro': '#D3D3D3',
        'Mel-de-orvalho-médio': '#98FB98',
        'Neve Claro': '#FFFAFA',
        'Neve Escuro': '#FFFAF0',
        'Neve Médio': '#FFFAF0',
        'Oliva-claro': '#808000',
        'Oliva-escuro': '#556B2F',
        'Oliva-médio': '#6B8E23',
        'Orquídea Claro': '#DA70D6',
        'Orquídea Escuro': '#9932CC',
        'Orquídea Médio': '#BA55D3',
        'Ouro Velho Claro': '#DAA520',
        'Ouro Velho Escuro': '#B8860B',
        'Ouro Velho Pálido': '#EEE8AA',
        'Peru Claro': '#CD853F',
        'Peru Escuro': '#8B5A2B',
        'Peru Médio': '#D2691E',
        'Pêssego-claro': '#FFDAB9',
        'Pêssego-escuro': '#FFCBA4',
        'Pêssego-médio': '#FFDAB9',
        'Prateado-claro': '#C0C0C0',
        'Prateado-escuro': '#808080',
        'Preto Fosco': '#0C0C0C',
        'Preto-azulado': '#000000',
        'Preto-azulado Médio': '#000000',
        'Preto-azulado-claro': '#000000',
        'Preto-azulado-escuro': '#000000',
        'Rosa Claro': '#FFC0CB',
        'Rosa Escuro': '#FF1493',
        'Rosa Médio': '#FFC0CB',
        'Rosa-antigo Claro': '#F778A1',
        'Rosa-antigo Escuro': '#8B2252',
        'Rosa-antigo Médio': '#C08081',
        'Roxo-claro': '#9370DB',
        'Roxo-escuro': '#800080',
        'Roxo-médio': '#9370DB',
        'Salmon Claro': '#FA8072',
        'Salmon Escuro': '#E9967A',
        'Salmon Médio': '#FF8C69',
        'Sienna Claro': '#A0522D',
        'Sienna Escuro': '#8B4513',
        'Sienna Médio': '#A0522D',
        'Tomate Claro': '#FF6347',
        'Tomate Escuro': '#CD4F39',
        'Tomate Médio': '#FF6347',
        'Trigo Claro': '#F5DEB3',
        'Trigo Escuro': '#D2B48C',
        'Trigo Médio': '#DAA520',
        'Turquesa Claro': '#00F5FF',
        'Turquesa Escuro': '#00CED1',
        'Turquesa Médio': '#40E0D0',
        'Turquesa Pálido': '#AFEEEE',
        'Verde Claro': '#00FF00',
        'Verde Escuro': '#008000',
        'Verde Floresta Claro': '#228B22',
        'Verde Floresta Escuro': '#006400',
        'Verde Floresta Médio': '#2E8B57',
        'Verde Grama Claro': '#7CFC00',
        'Verde Grama Escuro': '#7CFC00',
        'Verde Grama Médio': '#99FF99',
        'Verde Marinho Claro': '#20B2AA',
        'Verde Marinho Escuro': '#8FBC8F',
        'Verde Marinho Médio': '#3CB371',
        'Verde Oliva Claro': '#6B8E23',
        'Verde Oliva Escuro': '#556B2F',
        'Verde Oliva Médio': '#808000',
        'Verde Pálido': '#98FB98',
        'Verde Primavera Claro': '#00FF7F',
        'Verde Primavera Escuro': '#00FF00',
        'Verde Primavera Médio': '#00FA9A',
        'Verde-amarelado Claro': '#9ACD32',
        'Verde-amarelado Escuro': '#9ACD32',
        'Verde-amarelado Médio': '#ADFF2F',
        'Verde-amarelo Claro': '#ADFF2F',
        'Verde-amarelo Escuro': '#9ACD32',
        'Verde-amarelo Médio': '#9ACD32',
        'Verde-cartucho Claro': '#808000',
        'Verde-cartucho Escuro': '#556B2F',
        'Verde-cartucho Médio': '#808000',
        'Verde-lima Claro': '#32CD32',
        'Verde-lima Escuro': '#006400',
        'Verde-lima Médio': '#32CD32',
        'Vermelho Claro': '#FF0000',
        'Vermelho Escuro': '#8B0000',
        'Vermelho Indiano Claro': '#CD5C5C',
        'Vermelho Indiano Escuro': '#B0171F',
        'Vermelho Indiano Médio': '#CD5C5C',
        'Vermelho Violeta Claro': '#DB7093',
        'Vermelho Violeta Escuro': '#8B2252',
        'Vermelho Violeta Médio': '#C71585',
        'Whip de Papaia Claro': '#FFEFD5',
        'Whip de Papaia Escuro': '#FFE4B5',
        'Whip de Papaia Médio': '#FFE4B5'
    }
    return colors_database

def get_color_name(cor, colors_database):
    for color, value in colors_database.items():
        if value == cor:
            return color
    return None

def verificar_existencia_pasta(pasta_id):
    try:
        # URL da API do Google Drive para obter informações sobre um arquivo
        url = f"https://drive.google.com/drive/folders/{pasta_id}"
        
        # Faz uma chamada GET para a API do Google Drive
        response = requests.get(url)
        
        # Verifica o código de resposta
        if response.status_code == 200:
            return True  # A pasta existe
        else:
            return False  # A pasta não existe
    except Exception as e:
        return False  # Ocorreu um erro ao verificar a existência da pasta

async def suggest_channel_names(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    channel_names = [
        "┃💬┃chat",
        "┃💬┃ausente",
        "┃📊┃registro",
        "┃💥┃gringa",
        "┃📜┃gringa",
        "┃⌛┃tradução",
        "┃🎨┃raw",
        "┃✅┃editado",
        "┃💠┃revisado",
        "┃🌐┃glossário",
        "┃💠┃fontes",
        "┃📌┃drive",
        "┃📤┃drive",
        "┃📢┃avisos",
        "┃📅┃calendário",
        "┃📌┃utilidades",
        "┃📛┃ausência",
        "┃📚┃projetos",
        "┃🎎┃reunião",
        "┃💲┃folha-de-pagamento"

    ]
    return [
        app_commands.Choice(name=channel_name, value=channel_name)
        for channel_name in channel_names if current.lower() in channel_name.lower()
    ]

async def cores_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    colors_database = get_all_colors()
    choices = [
        app_commands.Choice(name=color, value=str(decimal))
        for color, decimal in colors_database.items() if current.lower() in color.lower()
    ]
    return choices

async def folder_id_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    server_id = interaction.guild.id
    configuracoes_pastas = carregar_configuracoes(server_id)
    choices = []
    for folder_id, config in configuracoes_pastas.items():
        comment = config.get('comment')
        autor = config.get('autor')
        criado = config.get('criado')
        if current.lower() in folder_id.lower() or current.lower() in comment.lower():
            name = f"{comment} | {folder_id} | {autor} | {criado}" if comment else folder_id
            choice = app_commands.Choice(name=name, value=folder_id)
            choices.append(choice)
    return choices

async def upload_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    choices = [
        app_commands.Choice(name="Enviar 1 arquivo por vez (não ocorre erros) (muito lento)", value="1"),
        app_commands.Choice(name="Enviar 2 arquivos por vez (provável) (lento)", value="2"),
        app_commands.Choice(name="Enviar 3 arquivos por vez (bem provável) (um pouco rápido)", value="3"),
        app_commands.Choice(name="Enviar 4 arquivos por vez (muito provável) (um pouco mais rápido)", value="4")
    ]
    return [
        choice for choice in choices
        if current.lower() in choice.name.lower()
    ]

async def tipo_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    choices = [
        app_commands.Choice(name="Pastas adicionadas", value="1"),
        app_commands.Choice(name="Arquivos processados", value="2"),
        app_commands.Choice(name="Comandos usados", value="3")
    ]
    return [
        choice for choice in choices
        if current.lower() in choice.name.lower()
    ]

async def modo_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    choices = [
        app_commands.Choice(name="Exportar", value="1"),
        app_commands.Choice(name="Importar", value="2"),
        app_commands.Choice(name="Ler", value="3")
    ]
    return [
        choice for choice in choices
        if current.lower() in choice.name.lower()
    ]












# Função para carregar as configurações das pastas a partir do arquivo JSON
def carregar_configuracoes_pastas():
    configuracoes_pastas2 = {}
    
    for file_name in os.listdir(server_drive):
        if file_name.endswith('_config.json'):
            server_id = file_name.split('_')[0]
            file_path = dir_inicial.joinpath(server_drive, file_name)
            with open(file_path) as config_file:
                config_data = json.load(config_file)
                pastas_config = config_data.get('pastas', {})
                configuracoes_pastas2[server_id] = pastas_config
    return configuracoes_pastas2

# Cria a instância da API do Google Drive
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

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
def enviar_mensagem_discord(name, link, created_time, last_modifying_user, pasta_id, server_id, configuracoes_pastas2):
    atual_server_id = server_id
    for server_id, pastas_config in configuracoes_pastas2.items():
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
def monitorar_pasta(pasta_id, server_id, configuracoes_pastas2):
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
                enviar_mensagem_discord(arquivo['name'], arquivo['webViewLink'], arquivo['createdTime'], arquivo['lastModifyingUser'], pasta_id, server_id, configuracoes_pastas2)

                arquivos_processados.add(arquivo['id'])

        page_token = response.get('nextPageToken')
        if not page_token:
            break  # Sai do loop quando não há mais páginas de resultados

    salvar_arquivos_processados(arquivos_processados, server_id)

async def executar_monitoramento():
    global monitoramento_ativo
    
    while True:
        if not monitoramento_ativo:
            break  # Interrompe o loop se o monitoramento estiver desligado
        
        configuracoes_pastas = carregar_configuracoes_pastas()
        for server_id, pastas_config in configuracoes_pastas.items():
            print(f"Configurações do servidor {server_id}:")
            pasta_ids = list(pastas_config.keys())  # IDs das pastas que deseja monitorar no Google Drive
            for pasta_id in pasta_ids:
                if not monitoramento_ativo:
                    break  # Interrompe o loop se o monitoramento estiver desligado

                # Exibir as configurações da pasta atual
                print(f"Pasta ID: {pasta_id}")
                print(f"Configurações: {json.dumps(pastas_config[pasta_id], indent=4)}\n\n\n")
                monitorar_pasta(pasta_id, server_id, configuracoes_pastas)
                await asyncio.sleep(1)  # Aguardar 1 segundo antes de verificar a próxima pasta    # padrão 10 segundos

        await asyncio.sleep(1)  # Aguardar 1 segundo antes de verificar a próxima pasta    # padrão 10 segundos










@tree1.command(name="ping", description="ver a latência do bot")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("ping", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    latency = client1.latency
    embed = discord.Embed(title="Pong! :ping_pong:",
                          description=f'Latência: {latency*1000:.2f} ms',
                          color=discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree1.command(name="version", description="mostra a versão")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("version", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    embed = discord.Embed(title="Versão", color=discord.Color.green())
    embed.add_field(name="Versão principal", value=f"**v{main_version}** :tada:", inline=False)
    embed.add_field(name="Versão do bot", value=f"**v{bot_version}** :tada:", inline=False)
    embed.add_field(name="Versão do drive", value=f"**Google API Core: v{google_api_core_version}** :tada:\n**Google API Python Client: v{google_api_python_client_version}** :tada:\n**Google auth: v{google_auth_version}** :tada:", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree1.command(name="runtime", description="tempo de execução")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("runtime", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    current_time = datetime.datetime.now()
    uptime = current_time - start_time
    
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_str = f"{days} dias, {hours} horas, {minutes} minutos, {seconds} segundos"
    
    embed = discord.Embed(title="Tempo de atividade", description=f"Tempo em execução: {uptime_str}", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, ephemeral=False)

@tree1.command(name="check_update", description="Este comando permite verificar e atualizar")
async def update(interaction: discord.Interaction, update: str = None):
    server_id = interaction.guild.id
    registrar_comando("check_update", interaction.user.name, server_id)    
    
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    get_uris()

    if update is None:
        update = "False"
    if update == "False":
        try:
            if not latest_version.startswith("v"):
                await interaction.response.send_message("A última latest não foi configurada corretamente.", ephemeral=True)
                return
            
            if latest_version == f"v{main_version}":
                await interaction.response.send_message(f"O bot está atualizado.\nVersão atual: v{main_version}", ephemeral=True)
            else:
                await interaction.response.send_message(f"O bot está desatualizado.\nVersão atual: v{main_version}\nVersão nova: {latest_version}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro ao verificar a atualização: {str(e)}", ephemeral=True)
    
    if update == "True":
        try:
            if not latest_version.startswith("v"):
                await interaction.response.send_message("A última latest não foi configurada corretamente.", ephemeral=True)
                return
            
            if not latest_version == f"v{main_version}":
                if os.path.exists("update.py"):
                    os.remove("update.py")
                urllib.request.urlretrieve(update_url, "update.py")
                await interaction.response.send_message("A atualização está sendo baixada e será iniciada em breve. Aguarde alguns segundos...", ephemeral=True)
                await client1.change_presence(status=discord.Status.offline)
                await client2.change_presence(status=discord.Status.offline)
                content = f"Servidor ID: {interaction.guild.id}\nCanal ID: {interaction.channel.id}"
                with open("last_channel.txt", "w") as file:
                    file.write(content)
                monitoring_stop()
                subprocess.Popen([f"{python_type}", "update.py"])

            else:
                await interaction.response.send_message(f"O bot já está atualizado.\nVersão atual: v{main_version}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro ao verificar a atualização: {str(e)}", ephemeral=True)

@update.autocomplete('update')
async def update_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    choices = [
        app_commands.Choice(name="Verificar", value="False"),
        app_commands.Choice(name="Atualizar", value="True")
    ]
    return [
        choice for choice in choices
        if current.lower() in choice.name.lower()
    ]

@tree2.command(name="help", description="comando de ajuda")
async def helps(interaction: discord.Interaction, comando: str = None):
    server_id = interaction.guild.id
    registrar_comando("help", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    if comando:
        # Verificar se o comando existe
        if comando not in ["criar", "configuracoes", "cor", "check_update", "import_config", "version", "ping", "uptime", "folder_add", "folder_remove", "folder_list", "monitoring_start", "monitoring_stop", "copy_config", "download_sites", "download_raw", "download_delete_cache", "log_comandos"]:
            await interaction.response.send_message(f"Comando '{comando}' não encontrado.", ephemeral=True)
            return
        
        if comando == "folder_add":
            embed = discord.Embed(title=comando, description="Adiciona uma nova pasta para ser verificada\nㅤ", color=discord.Color.blue())
            embed.add_field(name="folder_id (str)", value="ID da pasta do Google Drive", inline=False)
            embed.add_field(name="comment (str)", value="Nome da pasta", inline=False)
            embed.add_field(name="edit_link (str)", value="Link da pasta editados", inline=False)
            embed.add_field(name="project_link (str)", value="Link do projeto", inline=False)
            embed.add_field(name="raw_link (str, opcional)", value="Link da pasta RAW", inline=False)
            embed.add_field(name="canal (discord.TextChannel, opcional)", value="Canal onde vai ser notificado a pasta", inline=False)
            embed.add_field(name="avatar (str, opcional)", value="URL do avatar para a webhook", inline=False)
            embed.add_field(name="cor (str, autocomplete, opcional)", value="Cor associada à embed da webhook", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "folder_remove":
            embed = discord.Embed(title=comando, description="Remove uma pasta existente", color=discord.Color.blue())
            embed.add_field(name="folder_id (str, autocomplete)", value="ID da pasta do Google Drive", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "version":
            embed = discord.Embed(title=comando, description="Mostra a versão do bot", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "ping":
            embed = discord.Embed(title=comando, description="Mostra a latência atual do bot", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "uptime":
            embed = discord.Embed(title=comando, description="Mostra o tempo de execução do bot", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "folder_list":
            embed = discord.Embed(title=comando, description="Lista as IDs das pastas que já foram adicionadas para esse servidor ao qual foi usado o comando", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "copy_config":
            embed = discord.Embed(title=comando, description="É enviado um arquivo de configuração do servidor atual que foi usado o comando", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "log_comandos":
            embed = discord.Embed(title=comando, description="Mostra todos os comandos usados e por quem", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "download_sites":
            embed = discord.Embed(title=comando, description="Mostra os sites permitidos para serem usados no comando: `/download_raw`", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "download_raw":
            embed = discord.Embed(title=comando, description="Baixa capítulos de uma obra", color=discord.Color.blue())
            embed.add_field(name="link (str)", value="Link da obra ou capítulo", inline=False)
            embed.add_field(name="upload (int, autocomplete)", value="Quantidade de arquivos que vão ser upados ao mesmo tempo", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "download_delete_cache":
            embed = discord.Embed(title=comando, description="Limpa o cache dos downloads feitos", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "import_config":
            embed = discord.Embed(title=comando, description="Importa um arquivo de configuração de pastas para o servidor atual", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "criar":
            embed = discord.Embed(title=comando, description="Cria uma categoria e um ou vários canais nela", color=discord.Color.blue())
            embed.add_field(name="nome (str)", value="Nome da categoria", inline=False)
            embed.add_field(name="canal1 (str, autocomplete)", value="Nome do canal", inline=False)
            embed.add_field(name="canal2-20 (str, autocomplete, opcional)", value="Nome do canal", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "check_update":
            embed = discord.Embed(title=comando, description="Verifica atualizações e atualiza", color=discord.Color.blue())
            embed.add_field(name="update (str, autocomplete, opcional)", value="Verifica atualização ou atualiza para a versão mais recente", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "cor":
            embed = discord.Embed(title=comando, description="Escolha uma cor e ela será enviada como uma imagem da cor escolhida", color=discord.Color.blue())
            embed.add_field(name="cor (str)", value="Escolha uma cor", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "configuracoes":
            embed = discord.Embed(title=comando, description="Configurações para pastas", color=discord.Color.blue())
            embed.add_field(name="tipo (int)", value="Escolha o tipo de configuração", inline=False)
            embed.add_field(name="modo (int)", value="Escolha o modo da configuração", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "XXXXXXXXXXXXXXXXXXXXXX":
            embed = discord.Embed(title=comando, description="XXXXXXXXXXXXXXXXXXXXX", color=discord.Color.blue())
            embed.add_field(name="XXXXXXXXXXX", value="XXXXXXXXXXX", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    else:
        # Exibir lista de todos os comandos
        embed = discord.Embed(title="Comandos disponíveis", description="Lista de comandos disponíveis no bot", color=discord.Color.blue())
        embed.add_field(name="/version", value="Versão do bot", inline=False)
        embed.add_field(name="/ping", value="Verifica a latência do bot", inline=False)
        embed.add_field(name="/uptime", value="Mostra o tempo de execução do bot", inline=False)
        embed.add_field(name="/folder_add", value="Adiciona uma nova pasta", inline=False)
        embed.add_field(name="/folder_remove", value="Remove uma pasta existente", inline=False)
        embed.add_field(name="/folder_list", value="Lista de IDs na configuração", inline=False)
        embed.add_field(name="/monitoring_start", value="Inicia a verificação de pastas", inline=False)
        embed.add_field(name="/monitoring_stop", value="Para a verificação de pastas", inline=False)
        embed.add_field(name="/download_sites", value="Lista de sites permitidos", inline=False)
        embed.add_field(name="/download_raw", value="Baixa um raws", inline=False)
        embed.add_field(name="/download_delete_cache", value="Limpa o cache de downloads", inline=False)
        embed.add_field(name="/log_comandos", value="Verificar comandos que foram usados e por quem", inline=False)
        embed.add_field(name="/criar", value="Cria uma categoria e um ou vários canais nela", inline=False)
        embed.add_field(name="/check_update", value="Verifica atualizações e atualiza", inline=False)
        embed.add_field(name="/cor", value="Escolha uma cor e ela será enviada como uma imagem da cor escolhida", inline=False)
        embed.add_field(name="/configuracoes", value="Configurações para pastas", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@helps.autocomplete('comando')
async def helps_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    commands = sorted(["criar", "configuracoes", "cor","check_update", "import_config", "version", "ping", "uptime", "folder_add", "folder_remove", "folder_list", "monitoring_start", "monitoring_stop", "copy_config", "download_sites", "download_raw", "download_delete_cache", "log_comandos"])
    return [
        app_commands.Choice(name=comando, value=comando)
        for comando in commands if current.lower() in comando.lower()
    ]

@tree2.command(name="folder_add", description="adicionar pasta para ser verificada")
@app_commands.autocomplete(cor=cores_autocomplete)
async def slash_command(interaction: discord.Interaction, folder_id: str, comment: str, edit_link: str, project_link: str, raw_link: str = None, canal: discord.TextChannel = None, avatar: str = None, cor: str = None):
    server_id = interaction.guild.id
    registrar_comando(f"folder_add [{folder_id}]", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    # Verifica se o folder_id está em um dos formatos de link do Google Drive e extrai o ID
    if "drive.google.com" in folder_id:
        match = re.search(r"(?:/open\?id=|/folders/)([a-zA-Z0-9-_]+)", folder_id)
        if match:
            folder_id = match.group(1)
        else:
            return await interaction.response.send_message("ID da pasta inválido. Certifique-se de fornecer um ID válido do Google Drive.", ephemeral=True)

    # Verificar a existência da pasta
    pasta_existe = verificar_existencia_pasta(folder_id)
    if not pasta_existe:
        return await interaction.response.send_message("ID da pasta fornecida inválida.", ephemeral=True)
    
    await interaction.response.defer(ephemeral=True, thinking=True)

    try:
        # Verifica se o usuário forneceu o canal como argumento
        if not canal:
            canal = interaction.channel
        
        configuracoes_pastas = carregar_configuracoes(server_id)

        # Verifica se todos os argumentos foram fornecidos
        if any(arg is None for arg in [folder_id, comment, edit_link, project_link]):
            return await interaction.followup.send(f"Formato incorreto. Use o comando da seguinte forma:\n"
                                                            f"/folder_add <folder_id> <comment> <edit_link> <project_link> [raw_link] [canal] [avatar] [cor]", ephemeral=True)

        # Verifica se a pasta já existe nas configurações
        if folder_id in configuracoes_pastas:
            return await interaction.followup.send(f"A pasta com o ID {folder_id} já está configurada.", ephemeral=True)

        # Verifica se o comment é um nome válido, sem links
        if re.search(r"http*", comment):
            return await interaction.followup.send("O nome da pasta não pode conter links.", ephemeral=True)

        if cor:
            colors_database = get_all_colors()
            color_name = get_color_name(cor, colors_database)
            cor = cor.replace("#", "0x")
        else:
            color_name = None

        # Cria a webhook no canal especificado
        webhook = await canal.create_webhook(name=comment)

        if avatar:
            # Faz o download da imagem usando a biblioteca requests
            response = requests.get(avatar)
            response.raise_for_status()

            # Passa os bytes da imagem para o parâmetro avatar
            await webhook.edit(avatar=response.content)
        webhook_url = webhook.url

        autor = interaction.user.display_name
        
        # Obtém a data e hora atual
        agora = datetime.datetime.now()

        # Define o fuso horário de Brasília
        fuso_horario = pytz.timezone('America/Sao_Paulo')

        # Ajusta a data e hora para o fuso horário de Brasília
        agora_br = agora.astimezone(fuso_horario)

        # Formata a hora atual e a data atual
        hora_atual = agora_br.strftime("%H:%M:%S")
        dia_atual = agora_br.strftime("%d/%m/%Y")

        # Adiciona a nova pasta às configurações
        configuracoes_pastas[folder_id] = {
            'comment': comment,
            'webhook_url': webhook_url,
            'edit_link': edit_link,
            'project_link': project_link,
            'raw_link': raw_link,
            'webhook_id': webhook.id,
            'canal_id': canal.id,
            'avatar': avatar,
            'cor_name': color_name,
            'cor': cor,
            'autor': f'Criado por {autor}',
            'criado': f'{hora_atual} {dia_atual}'
        }

        salvar_configuracoes(configuracoes_pastas, server_id)

        await interaction.followup.send(f"A pasta com o ID **{folder_id}** foi adicionada com sucesso.", ephemeral=True)
    except commands.CheckAnyFailure:
        await interaction.followup.send("Você não tem permissão para executar este comando.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Ocorreu um erro ao adicionar a pasta: {str(e)}", ephemeral=True)

@tree2.command(name="folder_remove", description="remover pasta")
@app_commands.autocomplete(folder_id=folder_id_autocomplete)
async def slash_command(interaction: discord.Interaction, folder_id: str):
    server_id = interaction.guild.id
    registrar_comando(f"folder_remove [{folder_id}]", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True, thinking=True)

    if "/folders/" in folder_id:
        match = re.search(r"/folders/([a-zA-Z0-9-_]+)", folder_id)
        if match:
            folder_id = match.group(1)
        else:
            return await interaction.followup.send("URL da pasta inválida. Certifique-se de fornecer uma URL válida do Google Drive.", ephemeral=True)
    configuracoes_pastas = carregar_configuracoes(server_id)

    # Verifica se a pasta existe nas configurações
    if folder_id not in configuracoes_pastas:
        await interaction.followup.send(f"A pasta com o ID {folder_id} não está configurada.", ephemeral=True)
        return

    file_path = dir_inicial.joinpath(server_drive, f'{server_id}_config.json')

    if os.path.exists(file_path):
        with open(file_path) as config_file:
            data = json.load(config_file)

    if 'pastas' in data and folder_id in data['pastas']:
        comment = data['pastas'][folder_id].get('comment')
        canal_id = data['pastas'][folder_id].get('canal_id')
        if comment and canal_id:
            canal_id = client2.get_channel(canal_id)
            channel_webhooks = await canal_id.webhooks() 
            for webhook in channel_webhooks:
                if webhook.name == comment:
                    await webhook.delete()
                    break

    # Remove a pasta das configurações
    configuracoes_pastas.pop(folder_id)

    salvar_configuracoes(configuracoes_pastas, server_id)

    await interaction.followup.send(f"A pasta com o ID {folder_id} foi removida com sucesso.", ephemeral=True)

@tree2.command(name="monitoramento", description="alternar monitoramento de pastas")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("monitoring_toggle", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    global monitoramento_ativo
    
    if monitoramento_ativo:
        await interaction.response.send_message("A verificação de pastas foi parada com sucesso.", ephemeral=True)
        monitoramento_ativo = False  # Desligar o monitoramento
    else:
        monitoramento_ativo = True  # Ligado o monitoramento
        await interaction.response.send_message("A verificação de pastas foi iniciada com sucesso.", ephemeral=True)
        asyncio.create_task(executar_monitoramento())  # Iniciar o loop de verificação

@tree2.command(name="folder_list", description="lista de pastas adicionadas")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("folder_list", interaction.user.name, server_id)
    
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    configuracoes_pastas = carregar_configuracoes(server_id)

    if not configuracoes_pastas:
        await interaction.response.send_message("Nenhuma pasta foi adicionada para este servidor.", ephemeral=True)
        return

    embed = discord.Embed(title="Lista de Pastas", color=discord.Color.blue())
    for folder_id, folder_data in configuracoes_pastas.items():
        comment = folder_data.get('comment', 'N/A')
        embed.add_field(name="ID da pasta | Nome:", value=folder_id+' | '+comment, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree2.command(name="download_raw", description="baixa capitulos de obras")
@app_commands.autocomplete(upload=upload_autocomplete)
async def slash_command(interaction: discord.Interaction, link: str, upload: int):
    server_id = interaction.guild.id
    registrar_comando("download_raw", interaction.user.name, server_id)
    
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    if isinstance(upload, int):
    # Verificar se a variável é maior que 5
        if upload > 5:
            upload = 5
    else:
        upload = 1
    
    atualizar_valor_upload_config(upload)
    if "&" in link:
        link_sem_parametros = remove_parametro_no(link)
    else:
        link_sem_parametros = link
    print(link_sem_parametros)
    print(link)

    await verificar_link_e_baixar(interaction, link, link_sem_parametros)

@tree2.command(name="download_sites", description="sites permitidos para ser usados")
async def slash_command(interaction: discord.Integration):
    server_id = interaction.guild.id
    registrar_comando("download_sites", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    embed = discord.Embed(title="Sites disponíveis", description="Lista de sites permitidos para usar no comando `download_raw`", color=discord.Color.blue())
    embed.add_field(name="https://comic.naver.com/webtoon/", value="\n**Naver Webtoon**", inline=False)
    embed.add_field(name="https://www.webtoons.com/en/", value="\n**Webtoon**", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree2.command(name="download_delete_cache", description="apaga o cache de capítulos baixados")
async def slash_command(interaction: discord.Integration):
    server_id = interaction.guild.id
    registrar_comando("download_delete_cache", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    # Percorre todos os arquivos e subdiretórios dentro do diretório
    diretorio = "Obras"
    for item in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, item)
        if os.path.isfile(caminho_completo):
            # Remove o arquivo
            os.remove(caminho_completo)
        elif os.path.isdir(caminho_completo):
        # Remove o subdiretório e todo o seu conteúdo
            shutil.rmtree(caminho_completo)
    await interaction.response.send_message("Cache apagado!")

# Função para substituir 'null' por None no objeto JSON
def replace_null_with_none(obj):
    if isinstance(obj, list):
        return [replace_null_with_none(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: replace_null_with_none(value) for key, value in obj.items()}
    elif obj == 'null':
        return None
    else:
        return obj

@tree2.command(name="criar", description="cria uma categoria e vários canais nela")
@app_commands.autocomplete(canal1=suggest_channel_names, canal2=suggest_channel_names, canal3=suggest_channel_names, canal4=suggest_channel_names, canal5=suggest_channel_names, canal6=suggest_channel_names, canal7=suggest_channel_names, canal8=suggest_channel_names, canal9=suggest_channel_names, canal10=suggest_channel_names, canal11=suggest_channel_names, canal12=suggest_channel_names, canal13=suggest_channel_names, canal14=suggest_channel_names, canal15=suggest_channel_names, canal16=suggest_channel_names, canal17=suggest_channel_names, canal18=suggest_channel_names, canal19=suggest_channel_names, canal20=suggest_channel_names)
async def suggest_channel_names(interaction: discord.Interaction, nome: str, canal1: str, canal2: str = None, canal3: str = None, canal4: str = None, canal5: str = None, canal6: str = None, canal7: str = None, canal8: str = None, canal9: str = None, canal10: str = None, canal11: str = None, canal12: str = None, canal13: str = None, canal14: str = None, canal15: str = None, canal16: str = None, canal17: str = None, canal18: str = None, canal19: str = None, canal20: str = None):
    server_id = interaction.guild.id
    registrar_comando("criar", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True, thinking=True)

    canais = []
    for nome_canal in [canal1, canal2, canal3, canal4, canal5, canal6, canal7, canal8, canal9, canal10, canal11, canal12, canal13, canal14, canal15, canal16, canal17, canal18, canal19, canal20]:
        canais.append(nome_canal)

    guild = interaction.guild
    categoria = await guild.create_category_channel(nome)
    for nome_canal in canais:
        if not nome_canal is None:
            await guild.create_text_channel(nome_canal, category=categoria)
    
    canais = [canal for canal in canais if canal is not None]
    if len(canais) == 1:
        mensagem = "Categoria e canal criado com sucesso!"
    else:
        mensagem = "Categoria e canais criados com sucesso!"

    await interaction.followup.send(mensagem, ephemeral=True)

@tree2.command(name="cor", description="exibe a cor escolhida")
@app_commands.autocomplete(cor=cores_autocomplete)
async def slash_command(interaction: discord.Interaction, cor: str):
    server_id = interaction.guild.id
    registrar_comando("cor", interaction.user.name, server_id)
    
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    # Obtém a base de dados de cores
    colors_database = get_all_colors()

    cor_escolhida = next((k for k, v in colors_database.items() if v == cor), None)

    if cor_escolhida not in colors_database:
        await interaction.followup.send("Cor inválida. Verifique o nome da cor e tente novamente.", ephemeral=True)
        return

    valor_hexadecimal = colors_database[cor_escolhida]

    # Criar uma imagem 64x64 com a cor escolhida
    image = Image.new("RGB", (64, 64), valor_hexadecimal)

    # Salvar a imagem como um arquivo temporário
    temp_filename = "cor_temp.png"
    image.save(temp_filename)

    # Enviar a imagem no chat
    with open(temp_filename, "rb") as file:
        image_data = file.read()

    await interaction.followup.send(f"**{cor_escolhida}**\n***{valor_hexadecimal}***", file=discord.File(io.BytesIO(image_data), filename="cor.png"), ephemeral=True)

    # Remover o arquivo temporário
    os.remove(temp_filename)

@tree2.command(name="configuracoes", description="configurações para pastas")
@app_commands.autocomplete(tipo=tipo_autocomplete, modo=modo_autocomplete)
async def slash_command(interaction: discord.Interaction, tipo: int, modo: int):
    server_id = interaction.guild.id
    registrar_comando(f"configuracoes {tipo} {modo}", interaction.user.name, server_id)

    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    if tipo == 1:
        if modo == 1 or modo == 3:
            file_path = dir_inicial.joinpath(server_drive, f'{server_id}_config.json')
            if not os.path.exists(file_path):
                await interaction.followup.send("O arquivo de configuração para esse servidor não existe.", ephemeral=True)
                return

            try:
                await interaction.followup.send(file=discord.File(file_path), ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"Ocorreu um erro ao enviar o arquivo config.json: {str(e)}", ephemeral=True)
            return
        if modo == 2:
            await interaction.followup.send("Por favor, envie o arquivo de configuração para importar dentro de 1 minuto.", ephemeral=True)
            try:
                # Espera por 1 minuto para o arquivo ser enviado
                def check(message):
                    return message.author == interaction.user and message.attachments

                file_message = await client2.wait_for('message', timeout=60, check=check)

                attachment = file_message.attachments[0]

                # Faz o download do arquivo de configuração
                file_data = await attachment.read()

                # Carrega o conteúdo do arquivo de configuração
                config_data = json.loads(file_data)

                # Substitui 'null' por None no objeto JSON
                config_data = replace_null_with_none(config_data)

                # Verifica se o arquivo de configuração está no formato esperado
                if not isinstance(config_data, dict) or 'pastas' not in config_data:
                    await interaction.followup.send("O arquivo de configuração não contém configurações de pasta válidas. A importação foi cancelada.", ephemeral=True)
                    return

                configuracoes_pastas = carregar_configuracoes(server_id)

                # Verifica as pastas importadas e adiciona ao arquivo de configuração se não houver duplicatas
                pastas_importadas = config_data['pastas']
                pastas_adicionadas = []

                for pasta_id, pasta in pastas_importadas.items():
                    if isinstance(pasta, dict) and 'comment' in pasta and 'webhook_url' in pasta and 'edit_link' in pasta and 'project_link' in pasta and 'webhook_id' in pasta and 'canal_id' in pasta and 'autor' in pasta and 'criado' in pasta :
                        folder_id = pasta_id

                        # Verifica se a pasta já existe nas configurações
                        if folder_id in configuracoes_pastas:
                            await interaction.followup.send(f"A pasta com o ID ***{folder_id}*** já está configurada e foi ignorada.", ephemeral=True)
                        else:
                            commet = pasta.get('comment')
                            # Verifica se o campo 'raw_link' é 'null' e define como None
                            raw_link = pasta.get('raw_link')
                            if raw_link == 'null':
                                raw_link = None
                            avatar = pasta.get('avatar')
                            if avatar == 'null':
                                avatar = None
                            cor_name = pasta.get('cor_name')
                            if cor_name == 'null':
                                cor_name = None
                            cor = pasta.get('cor')
                            if cor == 'null':
                                cor = None
                            
                            canal_id = pasta['canal_id']
                            webhook_id = pasta['webhook_id']
                
                            # Verifica se a webhook existe
                            webhook = None
                            try:
                                webhook = await client2.fetch_webhook(webhook_id)
                            except discord.NotFound:
                                pass
                        
                            # Se a webhook não existir, cria uma nova
                            if not webhook:
                                canal = client2.get_channel(canal_id)
                                if canal:
                                    webhook = await canal.create_webhook(name=commet)

                                    if avatar:
                                    # Faz o download da imagem usando a biblioteca requests
                                        response = requests.get(avatar)
                                        response.raise_for_status()

                                        # Passa os bytes da imagem para o parâmetro avatar
                                        await webhook.edit(avatar=response.content)

                            # Verifica se a webhook foi encontrada ou criada com sucesso
                            if webhook:
                                # Atualiza o valor da webhook_url e webhook_id
                                pasta['webhook_url'] = webhook.url
                                pasta['webhook_id'] = webhook.id

                            configuracoes_pastas[folder_id] = {
                                'comment': pasta['comment'],
                                'webhook_url': pasta['webhook_url'],
                                'edit_link': pasta['edit_link'],
                                'project_link': pasta['project_link'],
                                'raw_link': raw_link,
                                'webhook_id':pasta['webhook_id'],
                                'canal_id':pasta['canal_id'],
                                'avatar':avatar,
                                'cor_name':cor_name,
                                'cor':cor,
                                'autor':pasta['autor'],
                                'criado':pasta['criado'],
                            }
                            pastas_adicionadas.append(folder_id)
                    else:
                        await file_message.delete()
                        await interaction.followup.send("Uma ou mais pastas importadas não possuem campos obrigatórios. A importação foi cancelada.", ephemeral=True)
                        return

                # Salva as configurações atualizadas no arquivo
                salvar_configuracoes(configuracoes_pastas, server_id)

                # Remove o arquivo enviado após a importação
                await file_message.delete()

                if len(pastas_adicionadas) > 0:
                    mensagem = "Configurações importadas com sucesso para as seguintes pastas:\n"
                    mensagem += "\n".join(pastas_adicionadas)
                else:
                    mensagem = "Nenhuma nova pasta foi adicionada. Todas as pastas importadas já estão configuradas."

                await interaction.followup.send(mensagem, ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("Você não tem permissão para executar esse comando.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Nenhum arquivo de configuração foi enviado. A importação foi cancelada.", ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"Ocorreu um erro ao importar o arquivo de configuração: {str(e)}", ephemeral=True)
            return

    if tipo == 2:
        if modo == 1 or modo == 3:
            arquivos_procesados_folder = dir_inicial.joinpath(arquivos_procesados)
            file = os.path.join(arquivos_procesados_folder, f"{server_id}_arquivos_processados.txt")
            try:
                await interaction.followup.send(file=discord.File(file, filename=f"{server_id}_arquivos_processados.txt"), ephemeral=True)
            except FileNotFoundError:
                await interaction.followup.send("O arquivo de arquivos processados não existe para este servidor.")
            return
        if modo == 2:
            arquivos_procesados_folder = dir_inicial.joinpath(arquivos_procesados)
            file = os.path.join(arquivos_procesados_folder, f"{server_id}_arquivos_processados.txt")
            await interaction.followup.send("Por favor, envie o arquivo para importar dentro de 1 minuto.", ephemeral=True)
            try:
                # Espera por 1 minuto para o arquivo ser enviado
                def check(message):
                    return message.author == interaction.user and message.attachments

                file_message = await client2.wait_for('message', timeout=60, check=check)

                attachment = file_message.attachments[0]

                # Faz o download do arquivo de configuração
                file_data = await attachment.read()
                file_data = file_data.decode("utf-8")  # Decodificar os dados do arquivo para uma string
                file_lines = file_data.splitlines()  # Dividir as linhas do arquivo
                file_content = "\n".join(file_lines)  # Unir as linhas novamente, usando \n como separador

                await file_message.delete()

                # Lê o arquivo de arquivos processados
                try:
                    with open(file, "r") as f:
                        arquivos_processados = f.read().splitlines()
                except FileNotFoundError:
                    arquivos_processados = []

                # Remove IDs repetidas do conteúdo do arquivo importado
                conteudo_importacao = file_lines.copy()
                for arquivo in arquivos_processados:
                    if arquivo in conteudo_importacao:
                        conteudo_importacao.remove(arquivo)

                # Adiciona as novas IDs ao arquivo de arquivos processados
                with open(file, "a") as f:
                    for arquivo in conteudo_importacao:
                        f.write(f"\n{arquivo}")

                # Verifica se foram adicionadas novas IDs
                if len(conteudo_importacao) > 0:
                    mensagem = "As seguintes IDs foram importadas com sucesso:\n"
                    mensagem += "\n".join(conteudo_importacao)
                else:
                    mensagem = "Nenhuma nova ID foi adicionada. As IDs importadas já estão no arquivo."

                await interaction.followup.send(mensagem, ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Nenhum arquivo de configuração foi enviado. A importação foi cancelada.", ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"Ocorreu um erro ao importar o arquivo de configuração: {str(e)}", ephemeral=True)
            return

    if tipo  == 3:
        if modo == 1:
            await interaction.followup.send("Você não pode exportar esse arquivo.", ephemeral=True)
            return
        if modo == 2:
            await interaction.followup.send("Você não pode importar nada para esse arquivo.", ephemeral=True)
            return
        if modo == 3:
                file_path = os.path.join(log_comandos, f'{server_id}_comandos.log')
                print(file_path)
                if not os.path.exists(file_path):
                    await interaction.followup.send("O arquivo não existe para este servidor.", ephemeral=True)
                    return
                try:
                    await interaction.followup.send(file=discord.File(file_path), ephemeral=True)
                    return
                except Exception as e:
                    await interaction.followup.send(f"Ocorreu um erro ao enviar o arquivo config.json: {str(e)}", ephemeral=True)
                    return

    await interaction.followup.send("Erro. Comando digitado incorretamente.", ephemeral=True)

loop.run_forever()