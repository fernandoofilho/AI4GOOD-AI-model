import os
import zipfile
from amazonia_legal import AmazoniaLegal

def unzip_all_in_directory(directory):
    """
    Descompacta todos os arquivos .zip dentro de um diretório.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
                extract_to = os.path.join(root, file.replace('.zip', ''))
                print(f"Descompactando {zip_path} para {extract_to}...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
                print(f"Arquivo {file} descompactado com sucesso.")

def process_amazonia_legal():
    """
    Itera por todas as pastas da Amazônia Legal e descompacta os arquivos.
    """
    for path in AmazoniaLegal.get_paths():
        absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
        if os.path.exists(absolute_path):
            print(f"Acessando diretório: {absolute_path}")
            unzip_all_in_directory(absolute_path)
        else:
            print(f"Diretório não encontrado: {absolute_path}")

if __name__ == "__main__":
    process_amazonia_legal()
