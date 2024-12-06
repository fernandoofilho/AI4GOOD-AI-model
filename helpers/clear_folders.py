import os
import shutil
from amazonia_legal import AmazoniaLegal

def move_csv_to_root(directory):
    """
    Move todos os arquivos .csv para o diretório raiz e exclui as pastas intermediárias e arquivos .zip.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                destination = os.path.join(directory, file)
                print(f"Movendo {file_path} para {destination}...")
                shutil.move(file_path, destination)
        
        if root != directory:
            for dir_ in dirs:
                dir_path = os.path.join(root, dir_)
                print(f"Removendo pasta {dir_path}...")
                shutil.rmtree(dir_path)

        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
                print(f"Removendo arquivo zip {zip_path}...")
                os.remove(zip_path)

def organize_amazonia_legal():
    """
    Organiza os arquivos .csv de todas as pastas da Amazônia Legal.
    """
    for path in AmazoniaLegal.get_paths():
        absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
        if os.path.exists(absolute_path):
            print(f"Organizando arquivos em: {absolute_path}")
            move_csv_to_root(absolute_path)
        else:
            print(f"Diretório não encontrado: {absolute_path}")

if __name__ == "__main__":
    organize_amazonia_legal()
