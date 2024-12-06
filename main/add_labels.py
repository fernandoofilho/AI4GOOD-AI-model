import sys
import os
import pandas as pd
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "helpers")))
from amazonia_legal import AmazoniaLegal


def process_focos_directory(directory):
    """
    Processa os arquivos na pasta dados/focos para filtrar bioma="Amazônia" e extrair dados relevantes.
    """
    processed_data = []

    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            print(f"Processando {file_path}...")

            # Carrega apenas as colunas necessárias em chunks
            chunks = pd.read_csv(
                file_path,
                chunksize=50000,
                usecols=["bioma", "municipio", "estado", "lat", "lon", "data_hora_gmt", "numero_dias_sem_chuva", "precipitacao"]
            )
            for chunk in chunks:
                # Filtra registros do bioma "Amazônia"
                filtered_chunk = chunk[chunk["bioma"] == "Amazônia"]
                processed_data.append(filtered_chunk)

    # Combina todos os chunks em um único DataFrame
    return pd.concat(processed_data, ignore_index=True)


def match_and_update_consolidado(consolidado_path, focos_data):
    """
    Faz o cruzamento do consolidado com os dados de focos e adiciona as colunas `numero_dias_sem_chuva` e `precipitacao`.
    """
    if not os.path.exists(consolidado_path):
        print(f"Arquivo não encontrado: {consolidado_path}")
        return

    print(f"Carregando {consolidado_path}...")

    # Carrega o consolidado
    consolidado = pd.read_csv(consolidado_path)

    # Verifica se as colunas obrigatórias estão presentes
    required_columns = ["municipio", "estado", "lat", "lon", "data_pas"]
    if not all(col in consolidado.columns for col in required_columns):
        print(f"Arquivo {consolidado_path} não contém todas as colunas necessárias: {required_columns}")
        return

    # Converte as colunas de data para datetime
    consolidado["data_pas"] = pd.to_datetime(consolidado["data_pas"])
    focos_data["data_hora_gmt"] = pd.to_datetime(focos_data["data_hora_gmt"])

    # Renomeia a coluna de data nos dados de focos para "data_pas" para facilitar o merge
    focos_data = focos_data.rename(columns={"data_hora_gmt": "data_pas"})

    # Faz o matching baseado em municipio, estado, lat, lon e data
    merged = pd.merge(
        consolidado,
        focos_data,
        on=["municipio", "estado", "lat", "lon", "data_pas"],
        how="left"
    )

    # Preenche valores faltantes
    merged["numero_dias_sem_chuva"] = merged["numero_dias_sem_chuva"].fillna(0).astype(int)
    merged["precipitacao"] = merged["precipitacao"].fillna(0).astype(float)

    # Salva o arquivo consolidado atualizado
    merged.to_csv(consolidado_path, index=False)
    print(f"Arquivo atualizado salvo em: {consolidado_path}")


def main():
    # Caminho para os arquivos focos
    focos_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dados", "focos"))
    print("Processando arquivos de focos...")

    # Processa os arquivos da pasta focos
    focos_data = process_focos_directory(focos_directory)

    # Caminho base para consolidado.csv
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dados"))

    # Itera sobre cada estado na Amazônia Legal
    for state_path in AmazoniaLegal.get_paths():
        relative_path = os.path.join(base_path, os.path.basename(state_path), "consolidado.csv")
        if os.path.exists(relative_path):
            print(f"Atualizando {relative_path}...")
            match_and_update_consolidado(relative_path, focos_data)
        else:
            print(f"Arquivo consolidado.csv não encontrado em: {relative_path}")


if __name__ == "__main__":
    main()
