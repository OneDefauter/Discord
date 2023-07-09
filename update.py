import urllib.request, requests, os, time, subprocess, psutil, shutil, sys, asyncio, platform
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

python_type = os.getenv('python_type')
GITHUB_REPO = "https://api.github.com/repos/OneDefauter/Discord"

update_url = None
drive_url = None
main__url = None
upload_arquivo_url = None
upload_files_url = None
download_e_up_url = None
latest_version = None
main_url = None

# Lista de nomes de processos que você deseja encerrar
process_names = ["main.py"]

def get_uris():
    global update_url
    global main_url
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
        if asset["name"] == "main.py":
            main_url = asset["browser_download_url"]
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

print("update")
def start_update():
    drive = dir_inicial.joinpath(src_drive_folder)
    download = dir_inicial.joinpath(src_download_folder)
    drive_path = os.path.join(drive, 'drive.py')
    main__path = os.path.join(download, 'main_.py')
    upload_arquivo_path = os.path.join(download, 'upload_arquivo.py')
    upload_files_path = os.path.join(download, 'upload_files.py')
    download_e_up_path = os.path.join(download, 'download_e_up.py')
    if os.path.exists("main.py"):
        os.remove("main.py")
        urllib.request.urlretrieve(main_url, "main.py")
    if os.path.exists(drive_path):
        os.remove(drive_path)
        urllib.request.urlretrieve(drive_url, drive_path)
    if not os.path.exists(main__path):
        os.remove(main__path)
        urllib.request.urlretrieve(main__url, main__path)
    if not os.path.exists(upload_arquivo_path):
        os.remove(upload_arquivo_path)
        urllib.request.urlretrieve(upload_arquivo_url, upload_arquivo_path)
    if not os.path.exists(upload_files_path):
        os.remove(upload_files_path)
        urllib.request.urlretrieve(upload_files_url, upload_files_path)
    if not os.path.exists(download_e_up_path):
        os.remove(download_e_up_path)
        urllib.request.urlretrieve(download_e_up_url, download_e_up_path)

# Encerra os processos
for proc in psutil.process_iter(['name', 'cmdline', 'pid']):
    for name in process_names:
        if proc.info['name'] == python_type and name in proc.info['cmdline']:
            pid = proc.info['pid']
            psutil.Process(pid).terminate()
            print(f"{name} - finalizado")

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


get_uris()
start_update()
comando = f'{python_type} main.py'
subprocess.Popen(comando, shell=True)
sys.exit()
print("Ainda em execução!")
print("Isso é um problema!")