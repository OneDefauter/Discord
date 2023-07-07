import json, subprocess, datetime, re, os, urllib.request, requests, discord, discord.ext, shutil, asyncio, sys, signal, pytz, platform, io
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
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

discord_process = None
main_version = "2.9"
bot_version = "2.3.0"
drive_version = "0.5.0"
GITHUB_REPO = "https://api.github.com/repos/OneDefauter/Discord"
drive_is_running = False

VERSION_FILE_URL = "https://github.com/OneDefauter/Discord/releases/download/bot/version.txt"
BOT_FILE_URL = "https://github.com/OneDefauter/Discord/releases/download/bot/bot.py"
DRIVE_FILE_URL = "https://github.com/OneDefauter/Discord/releases/download/bot/drive.py"

update_url = None
drive_url = None
main__url = None
upload_arquivo_url = None
upload_files_url = None
download_e_up_url = None
latest_version = None

def get_uris():
    global update_url
    global drive_url
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
        if asset["name"] == "drive.py":
            drive_url = asset["browser_download_url"]
        if asset["name"] == "main_.py":
            main__url = asset["browser_download_url"]
        if asset["name"] == "upload_arquivo.py":
            upload_arquivo_url = asset["browser_download_url"]
        if asset["name"] == "upload_files.py":
            upload_files_url = asset["browser_download_url"]
        if asset["name"] == "download_e_up.py":
            download_e_up_url = asset["browser_download_url"]

def start_files():
    drive = dir_inicial.joinpath(src_drive_folder)
    download = dir_inicial.joinpath(src_download_folder)
    
    if not os.path.exists(drive):
        os.makedirs(drive)
    if not os.path.exists(download):
        os.makedirs(download)
    drive_path = os.path.join(drive, 'drive.py')
    main__path = os.path.join(download, 'main_.py')
    upload_arquivo_path = os.path.join(download, 'upload_arquivo.py')
    upload_files_path = os.path.join(download, 'upload_files.py')
    download_e_up_path = os.path.join(download, 'download_e_up.py')

    if not os.path.exists(drive_path):
        print(drive_path)
        urllib.request.urlretrieve(drive_url, drive_path)
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
bot1 = loop.create_task(client1.start(bot_token1))
bot2 = loop.create_task(client2.start(bot_token2))

@client1.event
async def on_ready():
    await client1.change_presence(status=discord.Status.online)
    print('-------------------------------------------')
    print('Main')
    print(f'Bot conectado como {client1.user.name}')
    print('ID do Bot:', client1.user.id)
    print(f'VersÃ£o: {main_version}')
    print("Online: âœ…")
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
                print("Canal nÃ£o encontrado.")
        else:
            print("ID do servidor e/ou ID do canal nÃ£o encontrados.")

@client2.event
async def on_ready():
    await client2.change_presence(status=discord.Status.online)
    await client2.change_presence(activity=discord.Game(name="Drive: Desligado"))
    print('-------------------------------------------')
    print('Bot')
    print(f'Bot conectado como {client2.user.name}')
    print('ID do Bot:', client2.user.id)
    print(f'VersÃ£o: {bot_version}')
    print("Online: âœ…")
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
        print(f"Ocorreu um erro ao verificar a atualizaÃ§Ã£o: {str(e)}")
        return None

# Carrega as configuraÃ§Ãµes do arquivo config.json
def carregar_configuracoes(server_id):
    file_path = dir_inicial.joinpath(server_drive, f'{server_id}_config.json')

    if os.path.exists(file_path):
        with open(file_path) as config_file:
            config_data = json.load(config_file)
            return config_data.get('pastas', {})
    else:
        return {}

# Salva as configuraÃ§Ãµes no arquivo config.json
def salvar_configuracoes(configuracoes, server_id):
    file_path = dir_inicial.joinpath(server_drive, f'{server_id}_config.json')
    with open(file_path, 'w') as config_file:
        json.dump({'pastas': configuracoes}, config_file, indent=4)

async def verificar_link_e_baixar(interaction, link, link_sem_parametros):
    # Verificar se o link Ã© permitido
    links_permitidos = ["https://comic.naver.com/webtoon/","https://www.webtoons.com/en/"]
    if not any(link.startswith(permitido) for permitido in links_permitidos):
        await interaction.response.send_message("Desculpe, o link fornecido nÃ£o Ã© permitido.")
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
        
        # AutenticaÃ§Ã£o
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=scopes)
        drive_service = build('drive', 'v3', credentials=credentials)

        lista_pasta = drive_service.files().list(
            q=f"name='{pasta_link}' and parents='1af9Dg2ugnacDtj17gnTGhn-yi8Z9tuLc' and mimeType='application/vnd.google-apps.folder'",
            fields='files(id)'
        ).execute()

        if len(lista_pasta['files']) > 0:
            nova_pasta_id = lista_pasta['files'][0]['id']
            print(f'A pasta {pasta_link} jÃ¡ existe. Utilizando a pasta existente.')
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

        embed = discord.Embed(title=f"{get_name} ({pasta_link})",url=f"{link_sem_parametros}",description="**Os arquivos serÃ£o enviados neste** [**link aqui.**](https://drive.google.com/drive/folders/" + nova_pasta_id + "?usp=drive_link)",color=discord.Color.green())
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
        # Se o arquivo nÃ£o existir, crie um arquivo vazio
        with open(file_path, 'w') as arquivo:
            arquivo.write("{}")

    with open(file_path, 'r') as config_file:
        config = json.load(config_file)

    config['max_workers'] = upload

    with open(file_path, 'w') as config_file:
        json.dump(config, config_file)

def get_url_image(link_sem_parametros):
    # Faz a requisiÃ§Ã£o HTTP
    response = requests.get(link_sem_parametros)

    # ObtÃ©m o conteÃºdo HTML da pÃ¡gina
    html = response.content

    # Parseia o HTML usando o BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontra a tag <meta> com o atributo 'property' igual a 'og:image'
    meta_tag = soup.find('meta', attrs={'property': 'og:image'})

    # ObtÃ©m o valor do atributo 'content' da tag encontrada
    if meta_tag:
        image_url = meta_tag.get('content')
        return image_url

def get_url_name(link_sem_parametros):
    # Faz a requisiÃ§Ã£o HTTP
    response = requests.get(link_sem_parametros)

    # ObtÃ©m o conteÃºdo HTML da pÃ¡gina
    html = response.content

    # Parseia o HTML usando o BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontra a tag <meta> com o atributo 'property' igual a 'og:image'
    meta_tag = soup.find('meta', attrs={'property': 'og:title'})

    # ObtÃ©m o valor do atributo 'content' da tag encontrada
    if meta_tag:
        get_name = meta_tag.get('content')
        return get_name

def remove_parametro_no(link):
    # parse o URL
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    path_parts = parsed_url.path.split('/')
    
    # Se for um link naver, remove o parÃ¢metro 'no' (se ele existir)
    if "comic.naver.com" in link:
        if 'no' in query_params:
            del query_params['no']
    
    # Se for um link webtoon, reescreve o URL
    elif "webtoons.com" in link:
        # O path_parts tem o formato ['', 'en', 'genre', 'title', 'action', ...]
        # NÃ³s queremos reescrever para ['', 'en', 'genre', 'title', 'list']
        if len(path_parts) > 4:
            path_parts = path_parts[:4] + ['list']
            parsed_url = parsed_url._replace(path='/'.join(path_parts))
         
        # Remover o parÃ¢metro 'episode_no' da query string (se ele existir)
        if 'episode_no' in query_params:
            del query_params['episode_no']

    # Atualizar a query string sem o parÃ¢metro 'no' ou 'episode_no'
    parsed_url = parsed_url._replace(query=urlencode(query_params, doseq=True))

    # Reconstruir o URL sem o parÃ¢metro 'no' ou 'episode_no'
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
        'AmÃªndoa EsbranquiÃ§ada': '#FFEBCD',
        'Ameixa': '#DDA0DD',
        'Aqua': '#00FFFF',
        'Azul': '#0000FF',
        'Azul ArdÃ³sia': '#6A5ACD',
        'Azul ArdÃ³sia Claro': '#B0C4DE',
        'Azul ArdÃ³sia Escuro': '#483D8B',
        'Azul ArdÃ³sia MÃ©dio': '#7B68EE',
        'Azul AÃ§o': '#4682B4',
        'Azul AÃ§o Claro': '#B0E0E6',
        'Azul Cadete': '#5F9EA0',
        'Azul CÃ©u': '#87CEEB',
        'Azul CÃ©u Claro': '#87CEFA',
        'Azul CÃ©u Profundo': '#0000FF',
        'Azul Dodger': '#1E90FF',
        'Azul-marinho': '#000080',
        'Azul Meia-Noite': '#191970',
        'Azul PÃ³': '#AFEEEE',
        'Azul Royal': '#4169E1',
        'Azul Violeta': '#8A2BE2',
        'Azul-piscina': '#E0FFFF',
        'Azul CentÃ¡urea': '#6495ED',
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
        'Chiffon de LimÃ£o': '#FFFACD',
        'Chocolate': '#D2691E',
        'Ciano': '#00FFFF',
        'Ciano Claro': '#E0FFFF',
        'Ciano Escuro': '#008B8B',
        'Cinza': '#808080',
        'Cinza ArdÃ³sia': '#708090',
        'Cinza ArdÃ³sia Claro': '#B0C4DE',
        'Cinza ArdÃ³sia Escuro': '#2F4F4F',
        'Cinza Claro': '#D3D3D3',
        'Cinza Escuro': '#A9A9A9',
        'Cinza Fosco': '#696969',
        'Concha do Mar': '#FFF5EE',
        'Coral': '#FF7F50',
        'Coral Claro': '#F08080',
        'Creme de Menta': '#98FB98',
        'FumaÃ§a Branca': '#F5F5F5',
        'FÃºcsia': '#FF00FF',
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
        'OrquÃ­dea': '#DA70D6',
        'OrquÃ­dea Escuro': '#9932CC',
        'OrquÃ­dea MÃ©dio': '#BA55D3',
        'Ouro Velho': '#DAA520',
        'Ouro Velho Escuro': '#B8860B',
        'Ouro Velho PÃ¡lido': '#EEDD82',
        'Peru': '#CD853F',
        'Puff de PÃªssego': '#FFDAB9',
        'Prateado': '#C0C0C0',
        'Preto': '#000000',
        'Renda Antiga': '#A09E9C',
        'Rosa': '#FF69B4',
        'Rosa Claro': '#FFB6C1',
        'Rosa Empoeirado': '#FFE4E1',
        'Rosa Profundo': '#FF1493',
        'Rubor de Lavanda': '#FFAEB9',
        'Roxo': '#800080',
        'Roxo MÃ©dio': '#9370DB',
        'SalmÃ£o': '#FA8072',
        'SalmÃ£o Claro': '#FDAB9F',
        'SalmÃ£o Escuro': '#E9967A',
        'Sienna': '#A0522D',
        'Tomate': '#FF6347',
        'Trigo': '#D2B48C',
        'Turquesa': '#40E0D0',
        'Turquesa Escuro': '#00CED1',
        'Turquesa MÃ©dio': '#48D1CC',
        'Turquesa PÃ¡lido': '#AFEEEE',
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
        'Verde Marinho MÃ©dio': '#3D59AB',
        'Verde Oliva': '#6B8E23',
        'Verde Oliva Escuro': '#556B2F',
        'Verde PÃ¡lido': '#98FB98',
        'Verde Primavera': '#00FF7F',
        'Verde Primavera MÃ©dio': '#00FA9A',
        'Verde-lima': '#32CD32',
        'Vermelho': '#FF0000',
        'Vermelho Alaranjado': '#FF4500',
        'Vermelho Escuro': '#8B0000',
        'Vermelho Indiano': '#CD5C5C',
        'Vermelho Violeta': '#EE82EE',
        'Vermelho Violeta MÃ©dio': '#C71585',
        'Whip de Papaia': '#FFEFD5',
        'Azul Celeste': '#B2FFFF',
        'Azul Claro': '#ADD8E6',
        'Azul Escuro': '#00008B',
        'Azul Marinho MÃ©dio': '#000080',
        'Azul Marinho-claro': '#1974D2',
        'Azul Meia-Noite Claro': '#191970',
        'Azul Meia-Noite Escuro': '#000033',
        'Azul Meia-Noite MÃ©dio': '#191970',
        'Azul Meia-Noite-claro': '#2B65EC',
        'Azul Meia-Noite-escuro': '#003366',
        'Azul MÃ©dio': '#0000CD',
        'Azul PÃ¡lido': '#AFEEEE',
        'Azul-claro': '#87CEEB',
        'Azul-cÃ©u': '#87CEEB',
        'Azul-cÃ©u Claro': '#87CEFA',
        'Azul-cÃ©u Escuro': '#00BFFF',
        'Azul-cÃ©u MÃ©dio': '#6CA6CD',
        'Azul-dodger Claro': '#1E90FF',
        'Azul-dodger Escuro': '#0000C8',
        'Azul-dodger MÃ©dio': '#0000CD',
        'Azul-marinho Claro': '#000080',
        'Azul-marinho Escuro': '#000033',
        'Azul-marinho MÃ©dio': '#0000CD',
        'Azul-marinho-claro': '#4169E1',
        'Azul-marinho-escuro': '#00008B',
        'Azul-piscina Claro': '#ADD8E6',
        'Azul-piscina Escuro': '#66CDAA',
        'Azul-piscina MÃ©dio': '#00BFFF',
        'Cinza-claro': '#D3D3D3',
        'Cinza-escuro': '#A9A9A9',
        'Cinza-fosco': '#696969',
        'Coral-claro': '#F08080',
        'Coral-escuro': '#FF4500',
        'Creme-de-menta Claro': '#98FB98',
        'Creme-de-menta Escuro': '#90EE90',
        'Creme-de-menta MÃ©dio': '#00FA9A',
        'FÃºcsia Claro': '#FF00FF',
        'FÃºcsia Escuro': '#800080',
        'FÃºcsia MÃ©dio': '#FF00FF',
        'Laranja Claro': '#FFA500',
        'Laranja Escuro': '#FF8C00',
        'Laranja-claro': '#FF7F50',
        'Laranja-escuro': '#FF4500',
        'Lavanda Claro': '#E6E6FA',
        'Lavanda Escuro': '#9932CC',
        'Lavanda MÃ©dio': '#BA55D3',
        'Lavanda-claro': '#FFF0F5',
        'Lavanda-escuro': '#8B4789',
        'Lima Claro': '#00FF00',
        'Lima Escuro': '#008000',
        'Lima MÃ©dio': '#32CD32',
        'Marfim-claro': '#FFFFF0',
        'Marfim-escuro': '#FFFFE0',
        'Marrom-claro': '#D2B48C',
        'Marrom-escuro': '#8B4513',
        'Marrom-rosado': '#BC8F8F',
        'Marrom-sela': '#8B4513',
        'Mel-de-orvalho-claro': '#F5FFFA',
        'Mel-de-orvalho-escuro': '#D3D3D3',
        'Mel-de-orvalho-mÃ©dio': '#98FB98',
        'Neve Claro': '#FFFAFA',
        'Neve Escuro': '#FFFAF0',
        'Neve MÃ©dio': '#FFFAF0',
        'Oliva-claro': '#808000',
        'Oliva-escuro': '#556B2F',
        'Oliva-mÃ©dio': '#6B8E23',
        'OrquÃ­dea Claro': '#DA70D6',
        'OrquÃ­dea Escuro': '#9932CC',
        'OrquÃ­dea MÃ©dio': '#BA55D3',
        'Ouro Velho Claro': '#DAA520',
        'Ouro Velho Escuro': '#B8860B',
        'Ouro Velho PÃ¡lido': '#EEE8AA',
        'Peru Claro': '#CD853F',
        'Peru Escuro': '#8B5A2B',
        'Peru MÃ©dio': '#D2691E',
        'PÃªssego-claro': '#FFDAB9',
        'PÃªssego-escuro': '#FFCBA4',
        'PÃªssego-mÃ©dio': '#FFDAB9',
        'Prateado-claro': '#C0C0C0',
        'Prateado-escuro': '#808080',
        'Preto Fosco': '#0C0C0C',
        'Preto-azulado': '#000000',
        'Preto-azulado MÃ©dio': '#000000',
        'Preto-azulado-claro': '#000000',
        'Preto-azulado-escuro': '#000000',
        'Rosa Claro': '#FFC0CB',
        'Rosa Escuro': '#FF1493',
        'Rosa MÃ©dio': '#FFC0CB',
        'Rosa-antigo Claro': '#F778A1',
        'Rosa-antigo Escuro': '#8B2252',
        'Rosa-antigo MÃ©dio': '#C08081',
        'Roxo-claro': '#9370DB',
        'Roxo-escuro': '#800080',
        'Roxo-mÃ©dio': '#9370DB',
        'Salmon Claro': '#FA8072',
        'Salmon Escuro': '#E9967A',
        'Salmon MÃ©dio': '#FF8C69',
        'Sienna Claro': '#A0522D',
        'Sienna Escuro': '#8B4513',
        'Sienna MÃ©dio': '#A0522D',
        'Tomate Claro': '#FF6347',
        'Tomate Escuro': '#CD4F39',
        'Tomate MÃ©dio': '#FF6347',
        'Trigo Claro': '#F5DEB3',
        'Trigo Escuro': '#D2B48C',
        'Trigo MÃ©dio': '#DAA520',
        'Turquesa Claro': '#00F5FF',
        'Turquesa Escuro': '#00CED1',
        'Turquesa MÃ©dio': '#40E0D0',
        'Turquesa PÃ¡lido': '#AFEEEE',
        'Verde Claro': '#00FF00',
        'Verde Escuro': '#008000',
        'Verde Floresta Claro': '#228B22',
        'Verde Floresta Escuro': '#006400',
        'Verde Floresta MÃ©dio': '#2E8B57',
        'Verde Grama Claro': '#7CFC00',
        'Verde Grama Escuro': '#7CFC00',
        'Verde Grama MÃ©dio': '#99FF99',
        'Verde Marinho Claro': '#20B2AA',
        'Verde Marinho Escuro': '#8FBC8F',
        'Verde Marinho MÃ©dio': '#3CB371',
        'Verde Oliva Claro': '#6B8E23',
        'Verde Oliva Escuro': '#556B2F',
        'Verde Oliva MÃ©dio': '#808000',
        'Verde PÃ¡lido': '#98FB98',
        'Verde Primavera Claro': '#00FF7F',
        'Verde Primavera Escuro': '#00FF00',
        'Verde Primavera MÃ©dio': '#00FA9A',
        'Verde-amarelado Claro': '#9ACD32',
        'Verde-amarelado Escuro': '#9ACD32',
        'Verde-amarelado MÃ©dio': '#ADFF2F',
        'Verde-amarelo Claro': '#ADFF2F',
        'Verde-amarelo Escuro': '#9ACD32',
        'Verde-amarelo MÃ©dio': '#9ACD32',
        'Verde-cartucho Claro': '#808000',
        'Verde-cartucho Escuro': '#556B2F',
        'Verde-cartucho MÃ©dio': '#808000',
        'Verde-lima Claro': '#32CD32',
        'Verde-lima Escuro': '#006400',
        'Verde-lima MÃ©dio': '#32CD32',
        'Vermelho Claro': '#FF0000',
        'Vermelho Escuro': '#8B0000',
        'Vermelho Indiano Claro': '#CD5C5C',
        'Vermelho Indiano Escuro': '#B0171F',
        'Vermelho Indiano MÃ©dio': '#CD5C5C',
        'Vermelho Violeta Claro': '#DB7093',
        'Vermelho Violeta Escuro': '#8B2252',
        'Vermelho Violeta MÃ©dio': '#C71585',
        'Whip de Papaia Claro': '#FFEFD5',
        'Whip de Papaia Escuro': '#FFE4B5',
        'Whip de Papaia MÃ©dio': '#FFE4B5'
    }
    return colors_database

def get_color_name(cor, colors_database):
    for color, value in colors_database.items():
        if value == cor:
            return color
    return None

def verificar_existencia_pasta(pasta_id):
    try:
        # URL da API do Google Drive para obter informaÃ§Ãµes sobre um arquivo
        url = f"https://drive.google.com/drive/folders/{pasta_id}"
        
        # Faz uma chamada GET para a API do Google Drive
        response = requests.get(url)
        
        # Verifica o cÃ³digo de resposta
        if response.status_code == 200:
            return True  # A pasta existe
        else:
            return False  # A pasta nÃ£o existe
    except Exception as e:
        return False  # Ocorreu um erro ao verificar a existÃªncia da pasta

async def suggest_channel_names(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    channel_names = [
        "â”ƒðŸ’¬â”ƒchat",
        "â”ƒðŸ“Šâ”ƒregistro",
        "â”ƒðŸ’¥â”ƒgringa",
        "â”ƒðŸ“œâ”ƒgringa",
        "â”ƒâŒ›â”ƒtraduÃ§Ã£o",
        "â”ƒðŸŽ¨â”ƒraw",
        "â”ƒâœ…â”ƒeditado",
        "â”ƒðŸ’ â”ƒrevisado",
        "â”ƒðŸŒâ”ƒglossÃ¡rio",
        "â”ƒðŸ’ â”ƒfontes",
        "â”ƒðŸ“Œâ”ƒdrive",
        "â”ƒðŸ“¤â”ƒdrive",
        "â”ƒðŸ“¢â”ƒavisos",
        "â”ƒðŸ“…â”ƒcalendÃ¡rio",
        "â”ƒðŸ“Œâ”ƒutilidades",
        "â”ƒðŸ“›â”ƒausÃªncia",
        "â”ƒðŸ“šâ”ƒprojetos",
        "â”ƒðŸ’²â”ƒfolha-de-pagamento"

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
        app_commands.Choice(name="Enviar 1 arquivo por vez (nÃ£o ocorre erros) (muito lento)", value="1"),
        app_commands.Choice(name="Enviar 2 arquivos por vez (provÃ¡vel) (lento)", value="2"),
        app_commands.Choice(name="Enviar 3 arquivos por vez (bem provÃ¡vel) (um pouco rÃ¡pido)", value="3"),
        app_commands.Choice(name="Enviar 4 arquivos por vez (muito provÃ¡vel) (um pouco mais rÃ¡pido)", value="4")
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
        app_commands.Choice(name="Arquivos processados", value="2")
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
        app_commands.Choice(name="Importar", value="2")
    ]
    return [
        choice for choice in choices
        if current.lower() in choice.name.lower()
    ]






















@tree1.command(name="ping", description="ver a latÃªncia do bot")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("ping", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    latency = client1.latency
    embed = discord.Embed(title="Pong! :ping_pong:",
                          description=f'LatÃªncia: {latency*1000:.2f} ms',
                          color=discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree1.command(name="version", description="mostra a versÃ£o")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("version", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return
    
    embed = discord.Embed(title="VersÃ£o", color=discord.Color.green())
    embed.add_field(name="VersÃ£o principal", value=f"**v{main_version}** :tada:", inline=False)
    embed.add_field(name="VersÃ£o do bot", value=f"**v{bot_version}** :tada:", inline=False)
    embed.add_field(name="VersÃ£o do drive", value=f"**v{drive_version}** :tada:", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree1.command(name="runtime", description="tempo de execuÃ§Ã£o")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("runtime", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    current_time = datetime.datetime.now()
    uptime = current_time - start_time
    
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_str = f"{days} dias, {hours} horas, {minutes} minutos, {seconds} segundos"
    
    embed = discord.Embed(title="Tempo de atividade", description=f"Tempo em execuÃ§Ã£o: {uptime_str}", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, ephemeral=False)

@tree1.command(name="check_update", description="Este comando permite verificar e atualizar")
async def update(interaction: discord.Interaction, update: str = None):
    server_id = interaction.guild.id
    registrar_comando("check_update", interaction.user.name, server_id)    
    
    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    get_uris()

    if update is None:
        update = "False"
    if update == "False":
        try:
            if not latest_version.startswith("v"):
                await interaction.response.send_message("A Ãºltima latest nÃ£o foi configurada corretamente.")
                return

            if latest_version == main_version:
                await interaction.response.send_message(f"O bot estÃ¡ atualizado.\nVersÃ£o atual: {main_version}", ephemeral=True)
            else:
                await interaction.response.send_message(f"O bot estÃ¡ desatualizado.\nVersÃ£o atual: {main_version}\nVersÃ£o nova: {latest_version}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro ao verificar a atualizaÃ§Ã£o: {str(e)}", ephemeral=True)
    
    if update == "True":
        try:
            if not latest_version.startswith("v"):
                await interaction.response.send_message("A Ãºltima latest nÃ£o foi configurada corretamente.")
                return

            if not latest_version == main_version:
                if os.path.exists("update.py"):
                    os.remove("update.py")
                urllib.request.urlretrieve(update_url, "update.py")
                await interaction.response.send_message("A atualizaÃ§Ã£o estÃ¡ sendo baixada e serÃ¡ iniciada em breve. Aguarde alguns segundos...", ephemeral=True)
                await client1.change_presence(status=discord.Status.offline)
                await client2.change_presence(status=discord.Status.offline)
                content = f"Servidor ID: {interaction.guild.id}\nCanal ID: {interaction.channel.id}"
                with open("last_channel.txt", "w") as file:
                    file.write(content)
                monitoring_stop()
                subprocess.Popen([f"{python_type}", "update.py"])

            else:
                await interaction.response.send_message(f"O bot jÃ¡ estÃ¡ atualizado.\nVersÃ£o atual: {main_version}", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro ao verificar a atualizaÃ§Ã£o: {str(e)}", ephemeral=False)

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

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    if comando:
        # Verificar se o comando existe
        if comando not in ["criar", "configuracoes", "cor", "check_update", "import_config", "version", "ping", "uptime", "folder_add", "folder_remove", "folder_list", "monitoring_start", "monitoring_stop", "copy_config", "download_sites", "download_raw", "download_delete_cache", "log_comandos"]:
            await interaction.response.send_message(f"Comando '{comando}' nÃ£o encontrado.", ephemeral=True)
            return
        
        if comando == "folder_add":
            embed = discord.Embed(title=comando, description="Adiciona uma nova pasta para ser verificada\nã…¤", color=discord.Color.blue())
            embed.add_field(name="folder_id (str)", value="ID da pasta do Google Drive", inline=False)
            embed.add_field(name="comment (str)", value="Nome da pasta", inline=False)
            embed.add_field(name="edit_link (str)", value="Link da pasta editados", inline=False)
            embed.add_field(name="project_link (str)", value="Link do projeto", inline=False)
            embed.add_field(name="raw_link (str, opcional)", value="Link da pasta RAW", inline=False)
            embed.add_field(name="canal (discord.TextChannel, opcional)", value="Canal onde vai ser notificado a pasta", inline=False)
            embed.add_field(name="avatar (str, opcional)", value="URL do avatar para a webhook", inline=False)
            embed.add_field(name="cor (str, autocomplete, opcional)", value="Cor associada Ã  embed da webhook", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "folder_remove":
            embed = discord.Embed(title=comando, description="Remove uma pasta existente", color=discord.Color.blue())
            embed.add_field(name="folder_id (str, autocomplete)", value="ID da pasta do Google Drive", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "version":
            embed = discord.Embed(title=comando, description="Mostra a versÃ£o do bot", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "ping":
            embed = discord.Embed(title=comando, description="Mostra a latÃªncia atual do bot", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "uptime":
            embed = discord.Embed(title=comando, description="Mostra o tempo de execuÃ§Ã£o do bot", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "folder_list":
            embed = discord.Embed(title=comando, description="Lista as IDs das pastas que jÃ¡ foram adicionadas para esse servidor ao qual foi usado o comando", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "copy_config":
            embed = discord.Embed(title=comando, description="Ã‰ enviado um arquivo de configuraÃ§Ã£o do servidor atual que foi usado o comando", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "log_comandos":
            embed = discord.Embed(title=comando, description="Mostra todos os comandos usados e por quem", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "download_sites":
            embed = discord.Embed(title=comando, description="Mostra os sites permitidos para serem usados no comando: `/download_raw`", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "download_raw":
            embed = discord.Embed(title=comando, description="Baixa capÃ­tulos de uma obra", color=discord.Color.blue())
            embed.add_field(name="link (str)", value="Link da obra ou capÃ­tulo", inline=False)
            embed.add_field(name="upload (int, autocomplete)", value="Quantidade de arquivos que vÃ£o ser upados ao mesmo tempo", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "download_delete_cache":
            embed = discord.Embed(title=comando, description="Limpa o cache dos downloads feitos", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "import_config":
            embed = discord.Embed(title=comando, description="Importa um arquivo de configuraÃ§Ã£o de pastas para o servidor atual", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "criar":
            embed = discord.Embed(title=comando, description="Cria uma categoria e um ou vÃ¡rios canais nela", color=discord.Color.blue())
            embed.add_field(name="nome (str)", value="Nome da categoria", inline=False)
            embed.add_field(name="canal1 (str, autocomplete)", value="Nome do canal", inline=False)
            embed.add_field(name="canal2-20 (str, autocomplete, opcional)", value="Nome do canal", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "check_update":
            embed = discord.Embed(title=comando, description="Verifica atualizaÃ§Ãµes e atualiza", color=discord.Color.blue())
            embed.add_field(name="update (str, autocomplete, opcional)", value="Verifica atualizaÃ§Ã£o ou atualiza para a versÃ£o mais recente", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "cor":
            embed = discord.Embed(title=comando, description="Escolha uma cor e ela serÃ¡ enviada como uma imagem da cor escolhida", color=discord.Color.blue())
            embed.add_field(name="cor (str)", value="Escolha uma cor", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "configuracoes":
            embed = discord.Embed(title=comando, description="ConfiguraÃ§Ãµes para pastas", color=discord.Color.blue())
            embed.add_field(name="tipo (int)", value="Escolha o tipo de configuraÃ§Ã£o", inline=False)
            embed.add_field(name="modo (int)", value="Escolha o modo da configuraÃ§Ã£o", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if comando == "XXXXXXXXXXXXXXXXXXXXXX":
            embed = discord.Embed(title=comando, description="XXXXXXXXXXXXXXXXXXXXX", color=discord.Color.blue())
            embed.add_field(name="XXXXXXXXXXX", value="XXXXXXXXXXX", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    else:
        # Exibir lista de todos os comandos
        embed = discord.Embed(title="Comandos disponÃ­veis", description="Lista de comandos disponÃ­veis no bot", color=discord.Color.blue())
        embed.add_field(name="/version", value="VersÃ£o do bot", inline=False)
        embed.add_field(name="/ping", value="Verifica a latÃªncia do bot", inline=False)
        embed.add_field(name="/uptime", value="Mostra o tempo de execuÃ§Ã£o do bot", inline=False)
        embed.add_field(name="/folder_add", value="Adiciona uma nova pasta", inline=False)
        embed.add_field(name="/folder_remove", value="Remove uma pasta existente", inline=False)
        embed.add_field(name="/folder_list", value="Lista de IDs na configuraÃ§Ã£o", inline=False)
        embed.add_field(name="/monitoring_start", value="Inicia a verificaÃ§Ã£o de pastas", inline=False)
        embed.add_field(name="/monitoring_stop", value="Para a verificaÃ§Ã£o de pastas", inline=False)
        embed.add_field(name="/download_sites", value="Lista de sites permitidos", inline=False)
        embed.add_field(name="/download_raw", value="Baixa um raws", inline=False)
        embed.add_field(name="/download_delete_cache", value="Limpa o cache de downloads", inline=False)
        embed.add_field(name="/log_comandos", value="Verificar comandos que foram usados e por quem", inline=False)
        embed.add_field(name="/criar", value="Cria uma categoria e um ou vÃ¡rios canais nela", inline=False)
        embed.add_field(name="/check_update", value="Verifica atualizaÃ§Ãµes e atualiza", inline=False)
        embed.add_field(name="/cor", value="Escolha uma cor e ela serÃ¡ enviada como uma imagem da cor escolhida", inline=False)
        embed.add_field(name="/configuracoes", value="ConfiguraÃ§Ãµes para pastas", inline=False)
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
    registrar_comando("folder_add", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return
    
    # Verifica se o folder_id estÃ¡ em um dos formatos de link do Google Drive e extrai o ID
    if "drive.google.com" in folder_id:
        match = re.search(r"(?:/open\?id=|/folders/)([a-zA-Z0-9-_]+)", folder_id)
        if match:
            folder_id = match.group(1)
        else:
            return await interaction.response.send_message("ID da pasta invÃ¡lido. Certifique-se de fornecer um ID vÃ¡lido do Google Drive.", ephemeral=True)

    # Verificar a existÃªncia da pasta
    pasta_existe = verificar_existencia_pasta(folder_id)
    if not pasta_existe:
        return await interaction.response.send_message("ID da pasta fornecida invÃ¡lida.", ephemeral=True)
    
    await interaction.response.defer(ephemeral=True, thinking=True)

    try:
        # Verifica se o usuÃ¡rio forneceu o canal como argumento
        if not canal:
            canal = interaction.channel
        
        configuracoes_pastas = carregar_configuracoes(server_id)

        # Verifica se todos os argumentos foram fornecidos
        if any(arg is None for arg in [folder_id, comment, edit_link, project_link]):
            return await interaction.followup.send(f"Formato incorreto. Use o comando da seguinte forma:\n"
                                                            f"/folder_add <folder_id> <comment> <edit_link> <project_link> [raw_link] [canal] [avatar] [cor]", ephemeral=True)

        # Verifica se a pasta jÃ¡ existe nas configuraÃ§Ãµes
        if folder_id in configuracoes_pastas:
            return await interaction.followup.send(f"A pasta com o ID {folder_id} jÃ¡ estÃ¡ configurada.", ephemeral=True)

        # Verifica se o comment Ã© um nome vÃ¡lido, sem links
        if re.search(r"http*", comment):
            return await interaction.followup.send("O nome da pasta nÃ£o pode conter links.", ephemeral=True)

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

            # Passa os bytes da imagem para o parÃ¢metro avatar
            await webhook.edit(avatar=response.content)
        webhook_url = webhook.url

        autor = interaction.user.display_name
        
        # ObtÃ©m a data e hora atual
        agora = datetime.datetime.now()

        # Define o fuso horÃ¡rio de BrasÃ­lia
        fuso_horario = pytz.timezone('America/Sao_Paulo')

        # Ajusta a data e hora para o fuso horÃ¡rio de BrasÃ­lia
        agora_br = agora.astimezone(fuso_horario)

        # Formata a hora atual e a data atual
        hora_atual = agora_br.strftime("%H:%M:%S")
        dia_atual = agora_br.strftime("%d/%m/%Y")

        # Adiciona a nova pasta Ã s configuraÃ§Ãµes
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
        await interaction.followup.send("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Ocorreu um erro ao adicionar a pasta: {str(e)}", ephemeral=True)

@tree2.command(name="folder_remove", description="remover pasta")
@app_commands.autocomplete(folder_id=folder_id_autocomplete)
async def slash_command(interaction: discord.Interaction, folder_id: str):
    server_id = interaction.guild.id
    registrar_comando("folder_remove", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True, thinking=True)

    if "/folders/" in folder_id:
        match = re.search(r"/folders/([a-zA-Z0-9-_]+)", folder_id)
        if match:
            folder_id = match.group(1)
        else:
            return await interaction.followup.send("URL da pasta invÃ¡lida. Certifique-se de fornecer uma URL vÃ¡lida do Google Drive.", ephemeral=True)
    configuracoes_pastas = carregar_configuracoes(server_id)

    # Verifica se a pasta existe nas configuraÃ§Ãµes
    if folder_id not in configuracoes_pastas:
        await interaction.followup.send(f"A pasta com o ID {folder_id} nÃ£o estÃ¡ configurada.", ephemeral=True)
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

    # Remove a pasta das configuraÃ§Ãµes
    configuracoes_pastas.pop(folder_id)

    salvar_configuracoes(configuracoes_pastas, server_id)

    await interaction.followup.send(f"A pasta com o ID {folder_id} foi removida com sucesso.", ephemeral=True)

@tree2.command(name="monitoramento", description="alternar monitoramento de pastas")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("monitoring_toggle", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return
    
    global discord_process
    global drive_is_running
    
    if discord_process is None:
        await interaction.response.send_message("Iniciando a verificaÃ§Ã£o de pastas...", ephemeral=True)
        try:
            drive = dir_inicial.joinpath(src_drive_folder)
            drive_path = os.path.join(drive, 'drive.py')
            # Inicia o processo do drive.py
            discord_process = subprocess.Popen([f"{python_type}", drive_path])
        except Exception as e:
            await interaction.followup.send(f"Ocorreu um erro ao iniciar o drive.py: {str(e)}", ephemeral=True)
            discord_process = None
        else:
            drive_is_running = True
            await client2.change_presence(activity=discord.Game(name="Drive: Ligado"))
            await interaction.followup.send("O drive.py foi iniciado com sucesso.", ephemeral=True)
    else:
        await interaction.response.send_message("Parando a verificaÃ§Ã£o de pastas...", ephemeral=True)
        # Finaliza o processo do Discord.py
        discord_process.terminate()
        discord_process.wait()
        discord_process = None
        drive_is_running = False
        await client2.change_presence(activity=discord.Game(name="Drive: Desligado"))
        await interaction.followup.send("A verificaÃ§Ã£o de pastas foi parada com sucesso.", ephemeral=True)

@tree2.command(name="folder_list", description="lista de pastas adicionadas")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("folder_list", interaction.user.name, server_id)
    
    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
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
    
    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return
    
    if isinstance(upload, int):
    # Verificar se a variÃ¡vel Ã© maior que 5
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

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    embed = discord.Embed(title="Sites disponÃ­veis", description="Lista de sites permitidos para usar no comando `download_raw`", color=discord.Color.blue())
    embed.add_field(name="https://comic.naver.com/webtoon/", value="\n**Naver Webtoon**", inline=False)
    embed.add_field(name="https://www.webtoons.com/en/", value="\n**Webtoon**", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree2.command(name="download_delete_cache", description="apaga o cache de capÃ­tulos baixados")
async def slash_command(interaction: discord.Integration):
    server_id = interaction.guild.id
    registrar_comando("download_delete_cache", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    # Percorre todos os arquivos e subdiretÃ³rios dentro do diretÃ³rio
    diretorio = "Obras"
    for item in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, item)
        if os.path.isfile(caminho_completo):
            # Remove o arquivo
            os.remove(caminho_completo)
        elif os.path.isdir(caminho_completo):
        # Remove o subdiretÃ³rio e todo o seu conteÃºdo
            shutil.rmtree(caminho_completo)
    await interaction.response.send_message("Cache apagado!")

@tree2.command(name="log_comandos", description="mostra todos os comandos usados e por quem")
async def slash_command(interaction: discord.Interaction):
    server_id = interaction.guild.id
    registrar_comando("log_comandos", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    directory = 'server/log/comandos'
    file_path = os.path.join(directory, f'{server_id}_comandos.log')
    if not os.path.exists(file_path):
        await interaction.response.send_message("O arquivo comandos.log nÃ£o existe.", ephemeral=True)
        return

    try:
        await interaction.response.send_message(file=discord.File(file_path))
    except discord.Forbidden:
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar esse comando.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Ocorreu um erro ao enviar o arquivo config.json: {str(e)}", ephemeral=True)
    registrar_comando("log_comandos", interaction.user.name, server_id)

# FunÃ§Ã£o para substituir 'null' por None no objeto JSON
def replace_null_with_none(obj):
    if isinstance(obj, list):
        return [replace_null_with_none(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: replace_null_with_none(value) for key, value in obj.items()}
    elif obj == 'null':
        return None
    else:
        return obj

@tree2.command(name="criar", description="cria uma categoria e vÃ¡rios canais nela")
@app_commands.autocomplete(canal1=suggest_channel_names, canal2=suggest_channel_names, canal3=suggest_channel_names, canal4=suggest_channel_names, canal5=suggest_channel_names, canal6=suggest_channel_names, canal7=suggest_channel_names, canal8=suggest_channel_names, canal9=suggest_channel_names, canal10=suggest_channel_names, canal11=suggest_channel_names, canal12=suggest_channel_names, canal13=suggest_channel_names, canal14=suggest_channel_names, canal15=suggest_channel_names, canal16=suggest_channel_names, canal17=suggest_channel_names, canal18=suggest_channel_names, canal19=suggest_channel_names, canal20=suggest_channel_names)
async def suggest_channel_names(interaction: discord.Interaction, nome: str, canal1: str, canal2: str = None, canal3: str = None, canal4: str = None, canal5: str = None, canal6: str = None, canal7: str = None, canal8: str = None, canal9: str = None, canal10: str = None, canal11: str = None, canal12: str = None, canal13: str = None, canal14: str = None, canal15: str = None, canal16: str = None, canal17: str = None, canal18: str = None, canal19: str = None, canal20: str = None):
    server_id = interaction.guild.id
    registrar_comando("criar", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
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
    
    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    # ObtÃ©m a base de dados de cores
    colors_database = get_all_colors()

    cor_escolhida = next((k for k, v in colors_database.items() if v == cor), None)

    if cor_escolhida not in colors_database:
        await interaction.followup.send("Cor invÃ¡lida. Verifique o nome da cor e tente novamente.", ephemeral=True)
        return

    valor_hexadecimal = colors_database[cor_escolhida]

    # Criar uma imagem 64x64 com a cor escolhida
    image = Image.new("RGB", (64, 64), valor_hexadecimal)

    # Salvar a imagem como um arquivo temporÃ¡rio
    temp_filename = "cor_temp.png"
    image.save(temp_filename)

    # Enviar a imagem no chat
    with open(temp_filename, "rb") as file:
        image_data = file.read()

    await interaction.followup.send(f"**{cor_escolhida}**\n***{valor_hexadecimal}***", file=discord.File(io.BytesIO(image_data), filename="cor.png"), ephemeral=True)

    # Remover o arquivo temporÃ¡rio
    os.remove(temp_filename)

@tree2.command(name="configuracoes", description="configuraÃ§Ãµes para pastas")
@app_commands.autocomplete(tipo=tipo_autocomplete, modo=modo_autocomplete)
async def slash_command(interaction: discord.Interaction, tipo: int, modo: int):
    server_id = interaction.guild.id
    registrar_comando("configuracoes", interaction.user.name, server_id)

    # Verificar se o usuÃ¡rio tem a role "Drive" ou Ã© um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("VocÃª nÃ£o tem permissÃ£o para executar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    if tipo == 1:
        if modo == 1:
            file_path = dir_inicial.joinpath(server_drive, f'{server_id}_config.json')
            if not os.path.exists(file_path):
                await interaction.followup.send("O arquivo de configuraÃ§Ã£o para esse servidor nÃ£o existe.", ephemeral=True)
                return

            try:
                await interaction.followup.send(file=discord.File(file_path), ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"Ocorreu um erro ao enviar o arquivo config.json: {str(e)}", ephemeral=True)
            return
        if modo == 2:
            await interaction.followup.send("Por favor, envie o arquivo de configuraÃ§Ã£o para importar dentro de 1 minuto.", ephemeral=True)
            try:
                # Espera por 1 minuto para o arquivo ser enviado
                def check(message):
                    return message.author == interaction.user and message.attachments

                file_message = await client2.wait_for('message', timeout=60, check=check)

                attachment = file_message.attachments[0]

                # Faz o download do arquivo de configuraÃ§Ã£o
                file_data = await attachment.read()

                # Carrega o conteÃºdo do arquivo de configuraÃ§Ã£o
                config_data = json.loads(file_data)

                # Substitui 'null' por None no objeto JSON
                config_data = replace_null_with_none(config_data)

                # Verifica se o arquivo de configuraÃ§Ã£o estÃ¡ no formato esperado
                if not isinstance(config_data, dict) or 'pastas' not in config_data:
                    await interaction.followup.send("O arquivo de configuraÃ§Ã£o nÃ£o contÃ©m configuraÃ§Ãµes de pasta vÃ¡lidas. A importaÃ§Ã£o foi cancelada.", ephemeral=True)
                    return

                configuracoes_pastas = carregar_configuracoes(server_id)

                # Verifica as pastas importadas e adiciona ao arquivo de configuraÃ§Ã£o se nÃ£o houver duplicatas
                pastas_importadas = config_data['pastas']
                pastas_adicionadas = []

                for pasta_id, pasta in pastas_importadas.items():
                    if isinstance(pasta, dict) and 'comment' in pasta and 'webhook_url' in pasta and 'edit_link' in pasta and 'project_link' in pasta and 'webhook_id' in pasta and 'canal_id' in pasta and 'autor' in pasta and 'criado' in pasta :
                        folder_id = pasta_id
                
                        # Verifica se a pasta jÃ¡ existe nas configuraÃ§Ãµes
                        if folder_id in configuracoes_pastas:
                            await interaction.followup.send(f"A pasta com o ID ***{folder_id}*** jÃ¡ estÃ¡ configurada e foi ignorada.", ephemeral=True)
                        else:
                            # Verifica se o campo 'raw_link' Ã© 'null' e define como None
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
                        await interaction.followup.send("Uma ou mais pastas importadas nÃ£o possuem campos obrigatÃ³rios. A importaÃ§Ã£o foi cancelada.", ephemeral=True)
                        return

                # Salva as configuraÃ§Ãµes atualizadas no arquivo
                salvar_configuracoes(configuracoes_pastas, server_id)

                # Remove o arquivo enviado apÃ³s a importaÃ§Ã£o
                await file_message.delete()

                if len(pastas_adicionadas) > 0:
                    mensagem = "ConfiguraÃ§Ãµes importadas com sucesso para as seguintes pastas:\n"
                    mensagem += "\n".join(pastas_adicionadas)
                else:
                    mensagem = "Nenhuma nova pasta foi adicionada. Todas as pastas importadas jÃ¡ estÃ£o configuradas."

                await interaction.followup.send(mensagem, ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("VocÃª nÃ£o tem permissÃ£o para executar esse comando.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Nenhum arquivo de configuraÃ§Ã£o foi enviado. A importaÃ§Ã£o foi cancelada.", ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"Ocorreu um erro ao importar o arquivo de configuraÃ§Ã£o: {str(e)}", ephemeral=True)
            return

    if tipo == 2:
        if modo == 1:
            arquivos_procesados_folder = dir_inicial.joinpath(arquivos_procesados)
            file = os.path.join(arquivos_procesados_folder, f"{server_id}_arquivos_processados.txt")
            try:
                await interaction.followup.send(file=discord.File(file, filename=f"{server_id}_arquivos_processados.txt"), ephemeral=True)
            except FileNotFoundError:
                await interaction.followup.send("O arquivo de arquivos processados nÃ£o existe para este servidor.")
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

                # Faz o download do arquivo de configuraÃ§Ã£o
                file_data = await attachment.read()
                file_data = file_data.decode("utf-8")  # Decodificar os dados do arquivo para uma string
                file_lines = file_data.splitlines()  # Dividir as linhas do arquivo
                file_content = "\n".join(file_lines)  # Unir as linhas novamente, usando \n como separador

                await file_message.delete()

                # LÃª o arquivo de arquivos processados
                try:
                    with open(file, "r") as f:
                        arquivos_processados = f.read().splitlines()
                except FileNotFoundError:
                    arquivos_processados = []

                # Remove IDs repetidas do conteÃºdo do arquivo importado
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
                    mensagem = "Nenhuma nova ID foi adicionada. As IDs importadas jÃ¡ estÃ£o no arquivo."

                await interaction.followup.send(mensagem, ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Nenhum arquivo de configuraÃ§Ã£o foi enviado. A importaÃ§Ã£o foi cancelada.", ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"Ocorreu um erro ao importar o arquivo de configuraÃ§Ã£o: {str(e)}", ephemeral=True)
            return

    await interaction.response.send_message("Erro. Comando digitado incorretamente.", ephemeral=True)

loop.run_forever()