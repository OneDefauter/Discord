import json, subprocess, datetime, re, os, urllib.request, requests, discord, discord.ext, shutil, asyncio, sys, signal, pytz, platform, webcolors
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

start_time = datetime.datetime.now()

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
        urllib.request.urlretrieve("https://github.com/OneDefauter/Discord/releases/download/bot/drive.py", drive_path)
    if not os.path.exists(main__path):
        print(main__path)
        urllib.request.urlretrieve("https://github.com/OneDefauter/Discord/releases/download/bot/main_.py", main__path)
    if not os.path.exists(upload_arquivo_path):
        print(upload_arquivo_path)
        urllib.request.urlretrieve("https://github.com/OneDefauter/Discord/releases/download/bot/upload_arquivo.py", upload_arquivo_path)
    if not os.path.exists(upload_files_path):
        print(upload_files_path)
        urllib.request.urlretrieve("https://github.com/OneDefauter/Discord/releases/download/bot/upload_files.py", upload_files_path)
    if not os.path.exists(download_e_up_path):
        print(download_e_up_path)
        urllib.request.urlretrieve("https://github.com/OneDefauter/Discord/releases/download/bot/download_e_up.py", download_e_up_path)

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

start_files()
start_folders()

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
main_version = "2.7"
bot_version = "2.3.0"
drive_version = "0.5.0"

VERSION_FILE_URL = "https://github.com/OneDefauter/Discord/releases/download/bot/version.txt"
BOT_FILE_URL = "https://github.com/OneDefauter/Discord/releases/download/bot/bot.py"
DRIVE_FILE_URL = "https://github.com/OneDefauter/Discord/releases/download/bot/drive.py"

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
    await client1.change_presence(status=discord.Status.online)
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
        'Azul Alice': 15792383,
        'Branco Antigo': 16444375,
        'Aqua': 65535,
        'Água-marinha': 8388564,
        'Azul-piscina': 15794175,
        'Bege': 16119260,
        'Bisque': 16770244,
        'Preto': 0,
        'Amêndoa Esbranquiçada': 16772045,
        'Azul': 255,
        'Azul Violeta': 9055202,
        'Marrom': 10824234,
        'Madeira Burly': 14596231,
        'Azul Cadete': 6266528,
        'Verde-cartucho': 8388352,
        'Chocolate': 13789470,
        'Coral': 16744272,
        'Azul Centáurea': 6591981,
        'Seda de Milho': 16775388,
        'Carmesim': 14423100,
        'Ciano': 65535,
        'Azul Escuro': 139,
        'Ciano Escuro': 35723,
        'Ouro Velho Escuro': 12092939,
        'Cinza Escuro': 11119017,
        'Verde Escuro': 25600,
        'Caqui Escuro': 12433259,
        'Magenta Escuro': 9109643,
        'Verde Oliva Escuro': 5597999,
        'Laranja Escuro': 16747520,
        'Orquídea Escuro': 10040012,
        'Vermelho Escuro': 9109504,
        'Salmão Escuro': 15308410,
        'Verde Marinho Escuro': 9419919,
        'Azul Ardósia Escuro': 4734347,
        'Cinza Ardósia Escuro': 3100495,
        'Turquesa Escuro': 52945,
        'Violeta Escuro': 9699539,
        'Rosa Profundo': 16716947,
        'Azul Céu Profundo': 49151,
        'Cinza Fosco': 6908265,
        'Azul Dodger': 2003199,
        'Tijolo Fogo': 11674146,
        'Branco Floral': 16775920,
        'Verde Floresta': 2263842,
        'Fúcsia': 16711935,
        'Gainsboro': 14474460,
        'Branco Fantasma': 16316671,
        'Dourado': 16766720,
        'Ouro Velho': 14329120,
        'Cinza': 8421504,
        'Verde': 32768,
        'Verde-amarelo': 11403055,
        'Mel-de-orvalho': 15794160,
        'Rosa Vibrante': 16738740,
        'Vermelho Indiano': 13458524,
        'Índigo': 4915330,
        'Marfim': 16777200,
        'Caqui': 15787660,
        'Lavanda': 15132410,
        'Rubor de Lavanda': 16773365,
        'Verde Grama': 8190976,
        'Chiffon de Limão': 16775885,
        'Azul Claro': 11393254,
        'Coral Claro': 15761536,
        'Ciano Claro': 14745599,
        'Amarelo Ouro Velho Claro': 16448210,
        'Cinza Claro': 13882323,
        'Verde Claro': 9498256,
        'Rosa Claro': 16758465,
        'Salmão Claro': 16752762,
        'Verde Marinho Claro': 2142890,
        'Azul Céu Claro': 8900346,
        'Cinza Ardósia Claro': 7833753,
        'Azul Aço Claro': 11584734,
        'Amarelo Claro': 16777184,
        'Lima': 65280,
        'Verde-lima': 3329330,
        'Linho': 16445670,
        'Magenta': 16711935,
        'Marrom': 8388608,
        'Água-marinha Médio': 6737322,
        'Azul Médio': 205,
        'Orquídea Médio': 12211667,
        'Roxo Médio': 9662683,
        'Verde Marinho Médio': 3978097,
        'Azul Ardósia Médio': 8087790,
        'Verde Primavera Médio': 64154,
        'Turquesa Médio': 4772300,
        'Vermelho Violeta Médio': 13047173,
        'Azul Meia-Noite': 1644912,
        'Creme de Menta': 16121850,
        'Rosa Empoeirado': 16770273,
        'Mocassim': 16770229,
        'Branco Navajo': 16768685,
        'Azul-marinho': 128,
        'Renda Antiga': 16643558,
        'Oliva': 8421376,
        'Verde Oliva': 7048739,
        'Laranja': 16753920,
        'Vermelho Alaranjado': 16729344,
        'Orquídea': 14315734,
        'Ouro Velho Pálido': 15657130,
        'Verde Pálido': 10025880,
        'Turquesa Pálido': 11529966,
        'Vermelho Violeta Pálido': 14381203,
        'Whip de Papaia': 16773077,
        'Puff de Pêssego': 16767673,
        'Peru': 13468991,
        'Rosa': 16761035,
        'Ameixa': 14524637,
        'Azul Pó': 11591910,
        'Roxo': 8388736,
        'Vermelho': 16711680,
        'Marrom Rosado': 12357519,
        'Azul Royal': 4286945,
        'Marrom Sela': 9127187,
        'Salmão': 16416882,
        'Marrom Arenoso': 16032864,
        'Verde Marinho': 3050327,
        'Concha do Mar': 16774638,
        'Sienna': 10506797,
        'Prateado': 12632256,
        'Azul Céu': 8900331,
        'Azul Ardósia': 6970061,
        'Cinza Ardósia': 7372944,
        'Neve': 16775930,
        'Verde Primavera': 65407,
        'Azul Aço': 4620980,
        'Bronzeado': 13808780,
        'Verde-azulado': 32896,
        'Cardo': 14204888,
        'Tomate': 16737095,
        'Turquesa': 4251856,
        'Violeta': 15631086,
        'Trigo': 16113331,
        'Branco': 16777215,
        'Fumaça Branca': 16119285,
        'Amarelo': 16776960,
        'Verde-amarelado': 10145074,
    }
    return colors_database

def get_color_name(decimal_value, colors_database):
    for color, value in colors_database.items():
        if value == decimal_value:
            return color
    return None

def verificar_existencia_pasta(pasta_id):
    try:
        # Cria a instância da API do Google Drive
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=scopes)
        drive_service = build('drive', 'v3', credentials=credentials)

        # Verifica a existência da pasta
        drive_service.files().get(fileId=pasta_id).execute()

        # Fecha a instância do serviço
        drive_service.close()

        return True  # A pasta existe
    except Exception as e:
        return False  # A pasta não existe ou ocorreu um erro

async def suggest_channel_names(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    channel_names = [
        "┃💬┃chat",
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
        "┃💲┃folha-de-pagamento"

    ]
    return [
        app_commands.Choice(name=channel_name, value=channel_name)
        for channel_name in channel_names if current.lower() in channel_name.lower()
    ]












@tree1.command(name="ping", description="ver a latência do bot")
async def slash_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("ping", interaction.user.name, server_id)
    latency = client1.latency
    embed = discord.Embed(title="Pong! :ping_pong:",
                          description=f'Latência: {latency*1000:.2f} ms',
                          color=discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=False)

@tree1.command(name="version", description="mostra a versão")
async def slash_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("version", interaction.user.name, server_id)
    embed = discord.Embed(title="Versão", color=discord.Color.green())
    embed.add_field(name="Versão principal", value=f"**v{main_version}** :tada:", inline=False)
    embed.add_field(name="Versão do bot", value=f"**v{bot_version}** :tada:", inline=False)
    embed.add_field(name="Versão do drive", value=f"**v{drive_version}** :tada:", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=False)

@tree1.command(name="runtime", description="tempo de execução")
async def slash_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("runtime", interaction.user.name, server_id)
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
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("check_update", interaction.user.name, server_id)

    if update is None:
        update = "False"
    if update == "False":
        try:
            response = requests.get(VERSION_FILE_URL)
            response.raise_for_status()
            latest_version = response.text.strip().split("=")[1]

            if latest_version == main_version:
                await interaction.response.send_message(f"O bot está atualizado.\nVersão atual: {main_version}", ephemeral=False)
            else:
                await interaction.response.send_message(f"O bot está desatualizado.\nVersão atual: {main_version}\nVersão nova: {latest_version}", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro ao verificar a atualização: {str(e)}", ephemeral=False)
    
    if update == "True":
        try:
            # Obter a versão mais recente do bot a partir do arquivo de versão
            response = requests.get(VERSION_FILE_URL)
            response.raise_for_status()
            latest_version = response.text.strip().split("=")[1]

            if not latest_version == main_version:
                update_url = "https://github.com/OneDefauter/Discord/releases/download/bot/update.py"
                update_file = "update.py"
                if os.path.exists("update.py"):
                    os.remove("update.py")
                urllib.request.urlretrieve(update_url, update_file)
                await interaction.response.send_message("A atualização está sendo baixada e será iniciada em breve. Aguarde alguns segundos...", ephemeral=True)
                await client1.change_presence(status=discord.Status.offline)
                await client2.change_presence(status=discord.Status.offline)
                content = f"Servidor ID: {interaction.guild.id}\nCanal ID: {interaction.channel.id}"
                with open("last_channel.txt", "w") as file:
                    file.write(content)
                monitoring_stop()
                subprocess.Popen([f"{python_type}", update_file])

            else:
                await interaction.response.send_message(f"O bot já está atualizado.\nVersão atual: {main_version}", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro ao verificar a atualização: {str(e)}", ephemeral=False)

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
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("help", interaction.user.name, server_id)

    if comando:
        # Verificar se o comando existe
        if comando not in ["criar", "check_update", "import_config", "version", "ping", "uptime", "folder_add", "folder_remove", "folder_list", "monitoring_start", "monitoring_stop", "copy_config", "download_sites", "download_raw", "download_delete_cache", "log_comandos"]:
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
        embed.add_field(name="/copy_config", value="Envia o arquivo de configuração", inline=False)
        embed.add_field(name="/download_sites", value="Lista de sites permitidos", inline=False)
        embed.add_field(name="/download_raw", value="Baixa um raws", inline=False)
        embed.add_field(name="/download_delete_cache", value="Limpa o cache de downloads", inline=False)
        embed.add_field(name="/log_comandos", value="Verificar comandos que foram usados e por quem", inline=False)
        embed.add_field(name="/import_config", value="Importa um arquivo de configuração de pastas para o servidor atual", inline=False)
        embed.add_field(name="/criar", value="Cria uma categoria e um ou vários canais nela", inline=False)
        embed.add_field(name="/check_update", value="Verifica atualizações e atualiza", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@helps.autocomplete('comando')
async def helps_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    commands = sorted(["criar", "check_update", "import_config", "version", "ping", "uptime", "folder_add", "folder_remove", "folder_list", "monitoring_start", "monitoring_stop", "copy_config", "download_sites", "download_raw", "download_delete_cache", "log_comandos"])
    return [
        app_commands.Choice(name=comando, value=comando)
        for comando in commands if current.lower() in comando.lower()
    ]

@tree2.command(name="folder_add", description="adicionar pasta para ser verificada")
async def cores(interaction: discord.Interaction, folder_id: str, comment: str, edit_link: str, project_link: str, raw_link: str = None, canal: discord.TextChannel = None, avatar: str = None, cor: str = None):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("folder_add", interaction.user.name, server_id)
    
    # Verifica se o folder_id está em um dos formatos de link do Google Drive e extrai o ID
    if "drive.google.com" in folder_id:
        match = re.search(r"(?:/open\?id=|/folders/)([a-zA-Z0-9-_]+)", folder_id)
        if match:
            folder_id = match.group(1)
        else:
            return await interaction.response.send_message("ID da pasta inválido. Certifique-se de fornecer um ID válido do Google Drive.", ephemeral=False)

    # Verificar a existência da pasta
    pasta_existe = verificar_existencia_pasta(folder_id)
    if not pasta_existe:
        return await interaction.response.send_message("ID da pasta fornecida inválida.", ephemeral=False)

    try:
        # Verifica se o usuário forneceu o canal como argumento
        if not canal:
            canal = interaction.channel
        
        configuracoes_pastas = carregar_configuracoes(server_id)

        # Verifica se todos os argumentos foram fornecidos
        if any(arg is None for arg in [folder_id, comment, edit_link, project_link]):
            return await interaction.response.send_message(f"Formato incorreto. Use o comando da seguinte forma:\n"
                                                            f"/folder_add <folder_id> <comment> <edit_link> <project_link> [raw_link] [canal] [avatar]", ephemeral=False)

        # Verifica se a pasta já existe nas configurações
        if folder_id in configuracoes_pastas:
            return await interaction.response.send_message(f"A pasta com o ID {folder_id} já está configurada.", ephemeral=False)

        # Verifica se o comment é um nome válido, sem links
        if re.search(r"http*", comment):
            return await interaction.response.send_message("O nome da pasta não pode conter links.", ephemeral=False)

        if cor:
            decimal_value = int(cor)
            colors_database = get_all_colors()
            color_name = get_color_name(decimal_value, colors_database)
        else:
            color_name = None

        await interaction.response.defer()

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

        await interaction.followup.send(f"A pasta com o ID {folder_id} foi adicionada com sucesso.", ephemeral=False)
    except commands.CheckAnyFailure:
        await interaction.followup.send("Você não tem permissão para executar este comando.", ephemeral=False)
    except Exception as e:
        await interaction.followup.send(f"Ocorreu um erro ao adicionar a pasta: {str(e)}", ephemeral=False)

@cores.autocomplete('cor')
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

@tree2.command(name="folder_remove", description="remover pasta")
async def ids_folders(interaction: discord.Interaction, folder_id: str):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    await interaction.response.defer()
    server_id = interaction.guild.id
    registrar_comando("folder_remove", interaction.user.name, server_id)
    if "/folders/" in folder_id:
        match = re.search(r"/folders/([a-zA-Z0-9-_]+)", folder_id)
        if match:
            folder_id = match.group(1)
        else:
            return await interaction.followup.send("URL da pasta inválida. Certifique-se de fornecer uma URL válida do Google Drive.", ephemeral=False)
    configuracoes_pastas = carregar_configuracoes(server_id)

    # Verifica se a pasta existe nas configurações
    if folder_id not in configuracoes_pastas:
        await interaction.followup.send(f"A pasta com o ID {folder_id} não está configurada.", ephemeral=False)
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

    await interaction.followup.send(f"A pasta com o ID {folder_id} foi removida com sucesso.", ephemeral=False)

@ids_folders.autocomplete('folder_id')
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

@tree2.command(name="monitoring_start", description="iniciar monitoramento de pastas")
async def slash_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("monitoring_start", interaction.user.name, server_id)
    global discord_process
    
    if discord_process is not None:
        await interaction.response.send_message("A verificação de pastas já está em execução.", ephemeral=False)
        return
    
    await interaction.response.send_message("Iniciando a verificação de pastas...", ephemeral=False)
    
    try:
        # Inicia o processo do drive.py
        discord_process = subprocess.Popen([f"{python_type}", "drive.py"])
    except Exception as e:
        await interaction.followup.send(f"Ocorreu um erro ao iniciar o drive.py: {str(e)}", ephemeral=False)
        discord_process = None
    else:
        await interaction.followup.send("O drive.py foi iniciado com sucesso.", ephemeral=False)

@tree2.command(name="monitoring_stop", description="parar monitoramento de pastas")
async def slash_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("monitoring_stop", interaction.user.name, server_id)
    global discord_process
    
    if discord_process is None:
        await interaction.response.send_message("A verificação de pastas não está em execução.", ephemeral=False)
        return
    
    await interaction.response.send_message("Parando a verificação de pastas...", ephemeral=False)
    
    # Finaliza o processo do Discord.py
    discord_process.terminate()
    discord_process.wait()
    discord_process = None
    
    await interaction.followup.send("A verificação de pastas foi parado com sucesso.", ephemeral=False)

@tree2.command(name="copy_config", description="mostra o arquivo de configuração das pastas adicionadas")
async def slash_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("copy_config", interaction.user.name, server_id)
    directory = 'server/drive'
    file_path = os.path.join(directory, f'{server_id}_config.json')
    if not os.path.exists(file_path):
        await interaction.response.send_message("O arquivo config.json não existe.", ephemeral=True)
        return

    try:
        await interaction.response.send_message(file=discord.File(file_path))
    except discord.Forbidden:
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Ocorreu um erro ao enviar o arquivo config.json: {str(e)}", ephemeral=True)

@tree2.command(name="folder_list", description="lista de pastas adicionadas")
async def slash_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("folder_list", interaction.user.name, server_id)
    configuracoes_pastas = carregar_configuracoes(server_id)

    if not configuracoes_pastas:
        await interaction.response.send_message("Nenhuma pasta foi adicionada para este servidor.", ephemeral=False)
        return

    embed = discord.Embed(title="Lista de Pastas", color=discord.Color.blue())
    for folder_id, folder_data in configuracoes_pastas.items():
        comment = folder_data.get('comment', 'N/A')
        embed.add_field(name="ID da pasta | Nome:", value=folder_id+' | '+comment, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=False)

@tree2.command(name="download_raw", description="baixa capitulos de obras")
async def upload_upload(interaction: discord.Interaction, link: str, upload: int):
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
    
    server_id = interaction.guild.id
    registrar_comando("download_raw", interaction.user.name, server_id)
    atualizar_valor_upload_config(upload)
    if "&" in link:
        link_sem_parametros = remove_parametro_no(link)
    else:
        link_sem_parametros = link
    print(link_sem_parametros)
    print(link)

    await verificar_link_e_baixar(interaction, link, link_sem_parametros)

@upload_upload.autocomplete('upload')
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

@tree2.command(name="download_sites", description="sites permitidos para ser usados")
async def slash_command(interaction: discord.Integration):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("folder_add", interaction.user.name, server_id)
    embed = discord.Embed(title="Sites disponíveis", description="Lista de sites permitidos para usar no comando `download_raw`", color=discord.Color.blue())
    embed.add_field(name="https://comic.naver.com/webtoon/", value="\n**Naver Webtoon**", inline=False)
    embed.add_field(name="https://www.webtoons.com/en/", value="\n**Webtoon**", inline=False)
    await interaction.response.send_message(embed=embed)

@tree2.command(name="download_delete_cache", description="apaga o cache de capítulos baixados")
async def slash_command(interaction: discord.Integration):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("folder_add", interaction.user.name, server_id)
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

@tree2.command(name="log_comandos", description="mostra todos os comandos usados e por quem")
async def slash_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    directory = 'server/log/comandos'
    file_path = os.path.join(directory, f'{server_id}_comandos.log')
    if not os.path.exists(file_path):
        await interaction.response.send_message("O arquivo comandos.log não existe.", ephemeral=True)
        return

    try:
        await interaction.response.send_message(file=discord.File(file_path))
    except discord.Forbidden:
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Ocorreu um erro ao enviar o arquivo config.json: {str(e)}", ephemeral=True)
    registrar_comando("log_comandos", interaction.user.name, server_id)

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

@tree2.command(name="import_config", description="importa o arquivo de configuração das pastas adicionadas")
async def import_config_command(interaction: discord.Interaction):
    # Verificar se o usuário tem a role "Drive" ou é um administrador
    member = interaction.guild.get_member(interaction.user.id)
    is_drive_role = discord.utils.get(member.roles, name='Drive') is not None
    is_admin = member.guild_permissions.administrator

    if not (is_drive_role or is_admin):
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
        return
    
    server_id = interaction.guild.id
    registrar_comando("import_config", interaction.user.name, server_id)
    
    await interaction.response.send_message("Por favor, envie o arquivo de configuração para importar dentro de 1 minuto.", ephemeral=True)

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
            if isinstance(pasta, dict) and 'comment' in pasta and 'webhook_url' in pasta and 'edit_link' in pasta and 'project_link' in pasta:
                folder_id = pasta_id
                
                # Verifica se a pasta já existe nas configurações
                if folder_id in configuracoes_pastas:
                    await interaction.followup.send(f"A pasta com o ID ***{folder_id}*** já está configurada e foi ignorada.", ephemeral=False)
                else:
                    # Verifica se o campo 'raw_link' é 'null' e define como None
                    raw_link = pasta.get('raw_link')
                    if raw_link == 'null':
                        raw_link = None

                    configuracoes_pastas[folder_id] = {
                        'comment': pasta['comment'],
                        'webhook_url': pasta['webhook_url'],
                        'edit_link': pasta['edit_link'],
                        'project_link': pasta['project_link'],
                        'raw_link': raw_link
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

        await interaction.followup.send(mensagem, ephemeral=False)
    except discord.Forbidden:
        await interaction.followup.send("Você não tem permissão para executar esse comando.", ephemeral=True)
    except asyncio.TimeoutError:
        await interaction.followup.send("Nenhum arquivo de configuração foi enviado. A importação foi cancelada.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Ocorreu um erro ao importar o arquivo de configuração: {str(e)}", ephemeral=True)

@tree2.command(name="criar", description="cria uma categoria e vários canais nela")
@app_commands.autocomplete(canal1=suggest_channel_names, canal2=suggest_channel_names, canal3=suggest_channel_names, canal4=suggest_channel_names, canal5=suggest_channel_names, canal6=suggest_channel_names, canal7=suggest_channel_names, canal8=suggest_channel_names, canal9=suggest_channel_names, canal10=suggest_channel_names, canal11=suggest_channel_names, canal12=suggest_channel_names, canal13=suggest_channel_names, canal14=suggest_channel_names, canal15=suggest_channel_names, canal16=suggest_channel_names, canal17=suggest_channel_names, canal18=suggest_channel_names, canal19=suggest_channel_names, canal20=suggest_channel_names)
async def suggest_channel_names(interaction: discord.Interaction, nome: str, canal1: str, canal2: str = None, canal3: str = None, canal4: str = None, canal5: str = None, canal6: str = None, canal7: str = None, canal8: str = None, canal9: str = None, canal10: str = None, canal11: str = None, canal12: str = None, canal13: str = None, canal14: str = None, canal15: str = None, canal16: str = None, canal17: str = None, canal18: str = None, canal19: str = None, canal20: str = None):
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

loop.run_forever()