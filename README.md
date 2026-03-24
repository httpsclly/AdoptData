# AdoptData

Pipeline ETL em Python que coleta dados de animais em abrigos do condado de Sonoma (EUA) via API pública, limpa e analisa os dados, e salva os resultados.

## Etapas

### Extract
Faz uma requisição HTTP à API pública do abrigo de animais de Sonoma County e coleta até 10.000 registros em formato JSON, convertendo para um DataFrame do Pandas.

### Transform
- Remove a coluna `location` e elimina linhas duplicadas
- Converte `intake_date` e `outcome_date` para datetime
- Converte `days_in_shelter` para numérico
- Padroniza colunas de texto para Title Case e preenche nulos com "Desconhecido"
- Cria a coluna `ano` a partir da data de entrada

### EDA
Gera estatísticas no terminal (shape, nulos, contagens por tipo, raça e destino) e salva três gráficos em `data/output/`:
- `grafico_tipo.png` — animais por tipo
- `grafico_destino.png` — destinos mais comuns
- `grafico_ano.png` — entradas por ano

### Load
Salva os dados transformados em dois formatos:
- **CSV** (`AdoptData.csv`) — formato universal
- **Parquet** (`AdoptData.parquet`) — formato compacto e otimizado

## Como usar

```bash
pip install pandas matplotlib pyarrow
python data/AdoptData.py
```

## Estrutura

```
AdoptData/
├── README.md
├── requirements.txt
└── data/
    ├── AdoptData.py       # Pipeline principal
    └── output/            # Dados e gráficos gerados
```

## Tecnologias

Python, Pandas, Matplotlib, PyArrow
