import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
API_URL = "https://data.sonomacounty.ca.gov/resource/924a-vesw.json?$limit=10000"

COLUNAS_TEXTO = ["type", "breed", "color", "sex", "intake_type", "outcome_type"]
COLUNAS_DATA = ["intake_date", "outcome_date"]


# EXTRACT
def extract():
    print("[EXTRACT] Extraindo dados...")
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dados = json.loads(resp.read().decode("utf-8"))
    print(f"[EXTRACT] {len(dados)} registros extraídos.")
    return pd.DataFrame(dados)


# TRANSFORM
def transform(df):
    print("[TRANSFORM] Transformando dados...")
    df = df.drop(columns=["location"], errors="ignore").drop_duplicates()

    for col in COLUNAS_DATA:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "days_in_shelter" in df.columns:
        df["days_in_shelter"] = pd.to_numeric(df["days_in_shelter"], errors="coerce")

    for col in COLUNAS_TEXTO:
        if col in df.columns:
            df[col] = df[col].fillna("Desconhecido").str.strip().str.title()

    if "intake_date" in df.columns:
        df["ano"] = df["intake_date"].dt.year

    print(f"[TRANSFORM] {len(df)} linhas após transformação.")
    return df


# EDA
def salvar_grafico(dados, titulo, arquivo, kind="bar", color="steelblue", xlabel=None, ylabel="Quantidade"):
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_kwargs = {"kind": kind, "ax": ax, "color": color}
    if kind == "line":
        plot_kwargs["marker"] = "o"
    dados.plot(**plot_kwargs)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel or "")
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, arquivo))
    plt.close(fig)
    print(f"  Gráfico salvo: output/{arquivo}")


def eda(df):
    print("\n[EDA] Análise Exploratória")
    print(f"  Shape: {df.shape[0]} linhas x {df.shape[1]} colunas")

    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    print(f"  Nulos:\n{nulos.to_string()}" if not nulos.empty else "  Sem valores nulos.")

    if "days_in_shelter" in df.columns:
        print(f"  Dias no abrigo:\n{df['days_in_shelter'].describe().round(2).to_string()}")
    if "type" in df.columns:
        print(f"  Animais por tipo:\n{df['type'].value_counts().to_string()}")
    if "outcome_type" in df.columns:
        print(f"  Destino dos animais:\n{df['outcome_type'].value_counts().head(10).to_string()}")
    if "breed" in df.columns:
        print(f"  Top 10 raças:\n{df['breed'].value_counts().head(10).to_string()}")
    if "ano" in df.columns:
        print(f"  Entradas por ano:\n{df['ano'].value_counts().sort_index().to_string()}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if "type" in df.columns:
        salvar_grafico(df["type"].value_counts(), "Animais por Tipo", "grafico_tipo.png")
    if "outcome_type" in df.columns:
        salvar_grafico(df["outcome_type"].value_counts().head(8), "Destino dos Animais", "grafico_destino.png", kind="barh", color="coral", xlabel="Quantidade", ylabel="")
    if "ano" in df.columns:
        salvar_grafico(df["ano"].value_counts().sort_index(), "Entradas por Ano", "grafico_ano.png", kind="line", xlabel="Ano")

    print("[EDA] Análise concluída.")


# LOAD
def load(df):
    print("[LOAD] Salvando dados...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(os.path.join(OUTPUT_DIR, "AdoptData.csv"), index=False, encoding="utf-8-sig")
    df.to_parquet(os.path.join(OUTPUT_DIR, "AdoptData.parquet"), index=False)
    print("[LOAD] Dados salvos em output/")


# EXECUÇÃO
if __name__ == "__main__":
    df = extract()
    df = transform(df)
    eda(df)
    load(df)
    print("\nPipeline concluído!")
