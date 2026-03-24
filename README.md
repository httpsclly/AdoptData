# AdoptData - Projeto ETL

Projeto de estudo na área de Engenharia de Dados. Consiste em um pipeline ETL (Extract, Transform, Load) que coleta dados de um abrigo de animais do condado de Sonoma (Califórnia, EUA) através de uma API pública, transforma e analisa os dados, e os salva para uso posterior.

## O que é ETL?

ETL é um processo em 3 etapas para mover e preparar dados:

1. **Extract (Extrair)** — buscar os dados brutos na fonte
2. **Transform (Transformar)** — limpar e organizar os dados
3. **Load (Carregar)** — salvar os dados prontos para uso

---

## Etapas do Pipeline

### 1. Extract (Extração)

```python
def extract():
```

- Faz uma requisição HTTP à API pública do abrigo de animais de Sonoma County (`data.sonomacounty.ca.gov`)
- Coleta até 10.000 registros em formato JSON usando `urllib.request`
- Converte os dados para um DataFrame do Pandas
- Não requer autenticação nem chave de API

### 2. Transform (Transformação)

```python
def transform(df):
```

Nesta etapa os dados brutos são limpos e enriquecidos:

- **Remove coluna `location`** — descarta a coluna que contém dicionários aninhados
- **Remove duplicatas** — elimina linhas repetidas
- **Converte datas** — transforma `intake_date` e `outcome_date` em formato datetime
- **Converte numéricos** — transforma `days_in_shelter` em tipo numérico
- **Padroniza textos** — normaliza colunas como `type`, `breed`, `color`, `sex`, `intake_type` e `outcome_type` para formato Title Case, preenchendo nulos com "Desconhecido"
- **Extrai ano** — cria a coluna `ano` a partir da data de entrada no abrigo

### 3. EDA (Análise Exploratória)

```python
def eda(df):
```

Após a transformação, o pipeline executa uma análise exploratória automática que imprime no terminal:

- **Shape** — quantidade de linhas e colunas
- **Valores nulos** — campos que ainda possuem dados faltantes
- **Dias no abrigo** — estatísticas descritivas (média, mediana, min, max)
- **Animais por tipo** — contagem de cães, gatos, etc.
- **Destino dos animais** — top 10 tipos de desfecho (adoção, transferência, etc.)
- **Top 10 raças** — raças mais frequentes no abrigo
- **Entradas por ano** — evolução temporal dos registros

Também gera três gráficos salvos em `data/output/`:

- `grafico_tipo.png` — gráfico de barras com quantidade de animais por tipo
- `grafico_destino.png` — gráfico de barras horizontal com os destinos mais comuns
- `grafico_ano.png` — gráfico de linha com evolução de entradas por ano

### 4. Load (Carga)

```python
def load(df):
```

Salva os dados transformados em dois formatos dentro da pasta `data/output/`:

- **CSV** (`AdoptData.csv`) — formato universal, abre no Excel
- **Parquet** (`AdoptData.parquet`) — formato compacto e rápido, ideal para análise com Python

---

## Como usar

### Pré-requisitos

Instale as dependências:

```bash
pip install pandas matplotlib pyarrow
```

### Executar

```bash
python data/AdoptData.py
```

O pipeline vai extrair, transformar, analisar e salvar os dados automaticamente. Nenhuma configuração adicional é necessária — a API é pública e gratuita.

---

## Estrutura do Projeto

```
ETL - Projeto/
├── README.md              # Este arquivo
├── requirements.txt       # Dependências do Python
└── data/
    ├── AdoptData.py     # Pipeline ETL + EDA (código principal)
    └── output/            # Dados gerados (CSV, Parquet e gráficos)
```

---

## Tecnologias Utilizadas

- **Python 3** — linguagem principal
- **pandas** — manipulação e análise de dados
- **matplotlib** — geração de gráficos
- **urllib** — requisições HTTP (biblioteca padrão)
- **pyarrow** — exportação em formato Parquet
