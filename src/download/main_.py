import subprocess, sys, os, platform
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

python_type = os.getenv('python_type')

pasta_link = sys.argv[1]
nova_pasta_id = sys.argv[2]

if platform.system() == 'Windows':
    src_download_folder = 'src\\download'
else:
    src_download_folder = 'src/download'

dir_inicial = Path(os.getcwd())

# Lista de pastas locais e IDs das pastas no Google Drive para upload
pastas_upload = [
    {"pasta_local": "Obras\\"+pasta_link, "id_pasta_destino": nova_pasta_id}
    # Adicione mais pastas conforme necessário
]

# Chama o script de upload para cada pasta em paralelo
processes = []
for pasta in pastas_upload:
    file_path = dir_inicial.joinpath(src_download_folder, 'upload_files.py')
    comando = f'{python_type} "{file_path}" "{pasta["pasta_local"]}" "{pasta["id_pasta_destino"]}"'
    process = subprocess.Popen(comando, shell=True)
    processes.append(process)

# Espera todos os processos serem concluídos
for process in processes:
    process.wait()

print("Upload de arquivos concluído!")