import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "helpers")))
import pandas as pd
import geopandas as gpd
from datetime import timedelta
from scipy.spatial import cKDTree
import numpy as np
from amazonia_legal import AmazoniaLegal


def cluster_by_distance(df, max_distance_km=100):
    """
    Agrupa pontos de incêndio com base na distância geográfica usando cKDTree.
    """
    coords = np.array([(row.lat, row.lon) for _, row in df.iterrows()])
    tree = cKDTree(coords)
    clusters = tree.query_ball_tree(tree, max_distance_km / 110.574)  # 1° ≈ 110.574 km

    # Mapeia cada ponto a um cluster
    cluster_ids = [-1] * len(df)
    cluster_counter = 0

    for i, points in enumerate(clusters):
        if cluster_ids[i] == -1:  # Não foi agrupado ainda
            for p in points:
                cluster_ids[p] = cluster_counter
            cluster_counter += 1

    df["cluster"] = cluster_ids
    return df


def generate_nao_incendio(df):
    """
    Gera registros `não_incendio` com base nos intervalos de tempo sem incêndios em cada cluster.
    """
    nao_incendio_rows = []

    for cluster_id, group in df.groupby("cluster"):
        group = group.sort_values(by="data_pas")  # Ordena por data
        group["data_pas"] = pd.to_datetime(group["data_pas"])

        for i in range(len(group) - 1):
            current_row = group.iloc[i]
            next_row = group.iloc[i + 1]

            # Calcula intervalo de tempo
            interval_start = current_row["data_pas"]
            interval_end = next_row["data_pas"]

            # Se houver um intervalo de mais de um dia
            if interval_end - interval_start > timedelta(days=1):
                midpoint_lat = (current_row["lat"] + next_row["lat"]) / 2
                midpoint_lon = (current_row["lon"] + next_row["lon"]) / 2

                # Gera registros diários para o intervalo
                current_date = interval_start + timedelta(days=1)
                while current_date < interval_end:
                    nao_incendio_rows.append({
                        "lat": midpoint_lat,
                        "lon": midpoint_lon,
                        "data_pas": current_date,
                        "target": "não_incendio"
                    })
                    current_date += timedelta(days=1)

    nao_incendio_df = pd.DataFrame(nao_incendio_rows)
    return nao_incendio_df


def process_consolidado_file(csv_path):
    """
    Processa o consolidado.csv para criar registros de `não_incendio`.
    """
    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado: {csv_path}")
        return

    print(f"Processando {csv_path}...")

    # Carrega o arquivo CSV
    df = pd.read_csv(csv_path)

    # Filtra as colunas relevantes
    df["data_pas"] = pd.to_datetime(df["data_pas"])
    df["target"] = "incendio"

    # Clusteriza por distância
    df = cluster_by_distance(df)

    # Gera registros de `não_incendio`
    nao_incendio_df = generate_nao_incendio(df)

    # Combina registros de `incendio` e `não_incendio`
    combined_df = pd.concat([df, nao_incendio_df], ignore_index=True)

    # Salva o consolidado atualizado
    combined_df = combined_df.drop(columns=["cluster"], errors="ignore")
    combined_df.to_csv(csv_path, index=False)
    print(f"Arquivo atualizado salvo em: {csv_path}")


def process_all_states():
    """
    Itera por todas as pastas da Amazônia Legal e processa os arquivos `consolidado.csv`.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dados"))

    for path in AmazoniaLegal.get_paths():
        relative_path = os.path.join(base_path, os.path.basename(path), "consolidado.csv")
        if os.path.exists(relative_path):
            process_consolidado_file(relative_path)
        else:
            print(f"Arquivo consolidado.csv não encontrado em: {relative_path}")


if __name__ == "__main__":
    process_all_states()
