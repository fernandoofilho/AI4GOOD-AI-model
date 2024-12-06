import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "helpers")))
from amazonia_legal import AmazoniaLegal


def preprocess_data(df):
    """
    Pré-processa os dados:
    - Remove colunas desnecessárias.
    - Converte `data_pas` para datetime.
    - Adiciona variáveis sazonais.
    - Converte `target` para valores binários (0 e 1).
    """
    df = df.drop(columns=["pais"], errors="ignore")

    df["data_pas"] = pd.to_datetime(df["data_pas"])

    df["month"] = df["data_pas"].dt.month
    df["day_of_year"] = df["data_pas"].dt.dayofyear

    # transforma target em valores binários
    df["target"] = df["target"].map({"incendio": 1, "não_incendio": 0})
    if df["target"].isnull().any():
        raise ValueError("A coluna 'target' contém valores não reconhecidos após o mapeamento.")

    return df, df.drop(columns=["target"]), df["target"]


def temporal_train_test_split(df, date_column, test_ratio=0.3):
    """
    Realiza o split temporal, com base na coluna de tempo `date_column`.
    """
    df = df.sort_values(by=date_column)

    test_size = int(len(df) * test_ratio)
    train_df = df.iloc[:-test_size]
    test_df = df.iloc[-test_size:]

    X_train = train_df.drop(columns=["target", date_column])
    y_train = train_df["target"]
    X_test = test_df.drop(columns=["target", date_column])
    y_test = test_df["target"]

    return X_train, X_test, y_train, y_test


def save_model(model, model_name, results_dir, X_train):
    """
    Salva o modelo em formatos .pkl (Python) e .onnx (JavaScript).
    """
    model_dir = os.path.join(results_dir, model_name)
    os.makedirs(model_dir, exist_ok=True)

    # Salvar modelo em .pkl
    pkl_path = os.path.join(model_dir, f"{model_name}.pkl")
    joblib.dump(model, pkl_path)
    print(f"Modelo salvo em: {pkl_path}")

    # Converter e salvar modelo em .onnx (se possível)
    try:
        initial_type = [("float_input", FloatTensorType([None, X_train.shape[1]]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)
        onnx_path = os.path.join(model_dir, f"{model_name}.onnx")
        with open(onnx_path, "wb") as f:
            f.write(onnx_model.SerializeToString())
        print(f"Modelo salvo em formato ONNX: {onnx_path}")
    except Exception as e:
        print(f"Erro ao converter o modelo {model_name} para ONNX: {e}")


def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Treina e avalia três modelos: Random Forest, XGBoost e Logistic Regression.
    Salva os resultados na pasta results/{modelo}.
    """
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
    os.makedirs(results_dir, exist_ok=True)

    models = {
        "Random Forest": RandomForestClassifier(random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000)
    }

    results = {}

    for model_name, model in models.items():
        print(f"Treinando modelo: {model_name}...")
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        print(f"Acurácia de {model_name}: {acc:.2f}")

        report = classification_report(y_test, y_pred, output_dict=True)
        print(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        save_results(results_dir, model_name, cm, report)

        # Salvar o modelo
        save_model(model, model_name, results_dir, X_train)

        results[model_name] = {"modelo": model, "acurácia": acc}

    return results


def save_results(results_dir, model_name, cm, report):
    """
    Salva a matriz de confusão como PNG e as métricas como Excel.
    """
    model_dir = os.path.join(results_dir, model_name)
    os.makedirs(model_dir, exist_ok=True)

    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Não Incêndio", "Incêndio"], yticklabels=["Não Incêndio", "Incêndio"])
    plt.title(f"Matriz de Confusão - {model_name}")
    plt.ylabel("Real")
    plt.xlabel("Predito")
    png_path = os.path.join(model_dir, f"{model_name}_confusion_matrix.png")
    plt.savefig(png_path)
    plt.close()
    print(f"Matriz de confusão salva em: {png_path}")

    report_df = pd.DataFrame(report).transpose()
    excel_path = os.path.join(model_dir, f"{model_name}_metrics.xlsx")
    report_df.to_excel(excel_path, index=True)
    print(f"Métricas salvas em: {excel_path}")


def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dados"))

    dfs = []
    for path in AmazoniaLegal.get_paths():
        csv_path = os.path.join(base_path, os.path.basename(path), "consolidado_processado.csv")
        if os.path.exists(csv_path):
            dfs.append(pd.read_csv(csv_path))
        else:
            print(f"Arquivo não encontrado: {csv_path}")

    full_df = pd.concat(dfs, ignore_index=True)

    full_df, X, y = preprocess_data(full_df)
    X_train, X_test, y_train, y_test = temporal_train_test_split(full_df, "data_pas")

    print("Iniciando treinamento e avaliação dos modelos...")
    results = train_and_evaluate_models(X_train, X_test, y_train, y_test)

    best_model_name = max(results, key=lambda x: results[x]["acurácia"])
    print(f"Melhor modelo: {best_model_name} com acurácia {results[best_model_name]['acurácia']:.2f}")


if __name__ == "__main__":
    main()
