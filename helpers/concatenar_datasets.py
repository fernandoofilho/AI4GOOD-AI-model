import os
import pandas as pd
from amazonia_legal import AmazoniaLegal

def consolidate_csv_in_directory(directory):
    """
    Lê todos os arquivos .csv em um diretório que seguem o padrão ref_2023 ou ref_2024,
    concatena-os e salva um consolidado.csv, mantendo as colunas estado e municipio.
    """
    # Filtrar arquivos pelo padrão ref_2023.csv ou ref_2024.csv
    csv_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith("ref_2023.csv") or f.endswith("ref_2024.csv")
    ]

    if not csv_files:
        print(f"Nenhum arquivo CSV correspondente ao padrão encontrado em {directory}.")
        return

    print(f"Concatenando arquivos CSV em {directory}...")
    dataframes = []

    for csv_file in csv_files:
        print(f"Lendo {csv_file}...")

        # Lê o arquivo CSV
        df = pd.read_csv(csv_file)

        # Certifique-se de que as colunas estado e municipio estão presentes
        if "estado" not in df.columns or "municipio" not in df.columns:
            print(f"Atenção: Arquivo {csv_file} não contém as colunas 'estado' ou 'municipio'.")
        else:
            dataframes.append(df)

    # Concatena todos os DataFrames em um único
    consolidated_df = pd.concat(dataframes, ignore_index=True)

    # Salva o arquivo consolidado
    output_file = os.path.join(directory, "consolidado.csv")
    consolidated_df.to_csv(output_file, index=False)
    print(f"Arquivo consolidado salvo em {output_file}.")

def consolidate_amazonia_legal():
    """
    Itera por todas as pastas da Amazônia Legal e cria um consolidado.csv em cada uma.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dados"))

    for path in AmazoniaLegal.get_paths():
        relative_path = os.path.join(base_path, os.path.basename(path))
        if os.path.exists(relative_path):
            consolidate_csv_in_directory(relative_path)
        else:
            print(f"Diretório não encontrado: {relative_path}")

if __name__ == "__main__":
    consolidate_amazonia_legal()
