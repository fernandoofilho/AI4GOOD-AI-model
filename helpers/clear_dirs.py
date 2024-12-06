import os
from amazonia_legal import AmazoniaLegal

def remove_zips_and_empty_dirs(directory):
    """
    Remove todos os arquivos .zip e subpastas vazias em um diretório.
    """
    for root, dirs, files in os.walk(directory, topdown=False): 
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
                print(f"Removendo arquivo zip: {zip_path}")
                os.remove(zip_path)

        for dir_ in dirs:
            dir_path = os.path.join(root, dir_)
            if not os.listdir(dir_path): 
                print(f"Removendo pasta vazia: {dir_path}")
                os.rmdir(dir_path)

def clean_amazonia_legal():
    """
    Itera por todas as pastas da Amazônia Legal e limpa arquivos .zip e subpastas vazias.
    """
    for path in AmazoniaLegal.get_paths():
        absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
        if os.path.exists(absolute_path):
            print(f"Limpando diretório: {absolute_path}")
            remove_zips_and_empty_dirs(absolute_path)
        else:
            print(f"Diretório não encontrado: {absolute_path}")

if __name__ == "__main__":
    clean_amazonia_legal()
