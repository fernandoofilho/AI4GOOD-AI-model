import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "helpers")))
from amazonia_legal import AmazoniaLegal
from sklearn.preprocessing import MinMaxScaler
import pandas as pd




def fill_missing_values(df):
    """
    Preenche valores faltantes nas colunas numéricas com a média dos grupos baseados em
    `target`, `municipio` e datas semelhantes.
    """
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns

    for column in numeric_columns:
        if df[column].isna().sum() > 0:
            # Agrupamento por target, municipio e data truncada para o nível diário
            df[column] = df.groupby(
                [df["target"], df["municipio"], df["data_pas"].dt.date]
            )[column].transform(lambda x: x.fillna(x.mean()))

    # Preenche valores remanescentes com a média geral da coluna
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    return df


def normalize_data(df):
    """
    Normaliza as colunas numéricas para a faixa [0, 1] usando Min-Max Scaling.
    """
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns

    # Normalização com MinMaxScaler
    scaler = MinMaxScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df


def preprocess_csv(csv_path):
    """
    Processa o arquivo consolidado.csv:
    - Trata valores faltantes.
    - Normaliza os dados numéricos.
    - Remove colunas desnecessárias.
    """
    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado: {csv_path}")
        return

    print(f"Processando {csv_path}...")

    # Carrega os dados
    df = pd.read_csv(csv_path)
    df["data_pas"] = pd.to_datetime(df["data_pas"])

    # Tratamento de valores faltantes
    df = fill_missing_values(df)

    # Normalização dos dados
    df = normalize_data(df)

    # Remoção de colunas desnecessárias
    columns_to_drop = ["estado", "municipio", "foco_id", "id_bdq", "bioma_x", "bioma_y"]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors="ignore")

    # Salva o arquivo atualizado
    output_file = os.path.join(os.path.dirname(csv_path), "consolidado_processado.csv")
    df.to_csv(output_file, index=False)
    print(f"Arquivo processado salvo em: {output_file}")


def preprocess_all_states():
    """
    Itera por todas as pastas da Amazônia Legal e processa os arquivos consolidado.csv.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dados"))

    for path in AmazoniaLegal.get_paths():
        relative_path = os.path.join(base_path, os.path.basename(path), "consolidado.csv")
        if os.path.exists(relative_path):
            preprocess_csv(relative_path)
        else:
            print(f"Arquivo consolidado.csv não encontrado em: {relative_path}")


if __name__ == "__main__":
    preprocess_all_states()