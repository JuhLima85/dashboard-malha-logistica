import pandas as pd
from openpyxl import load_workbook

arquivo = r"C:\Users\diorgenes.souza\Downloads\Base Malha Diorgenes.xlsx"

print("Abrindo planilha...")

# Abre somente para identificar a primeira aba
wb = load_workbook(arquivo, read_only=True, data_only=True)
ws = wb["Base"]

# Linha 3 é o cabeçalho
cabecalho = next(
    ws.iter_rows(
        min_row=3,
        max_row=3,
        values_only=True
    )
)

# Lê somente os primeiros 10.000 registros
dados = []

for linha in ws.iter_rows(
    min_row=4,
    max_row=10003,
    values_only=True
):
    dados.append(linha)

wb.close()

df = pd.DataFrame(dados, columns=cabecalho)

# ==========================================================
# PROTÓTIPO - DIVISÃO DOS 10.000 REGISTROS POR MODAL
# 5.000 Rodoviário
# 5.000 Aéreo
# ==========================================================

df["Modal"] = "Rodoviario"

df.loc[df.index >= 5000, "Modal"] = "Aereo"

print()
print("Distribuição por modal:")
print(df["Modal"].value_counts())

print(f"Linhas carregadas: {len(df)}")
print(f"Colunas: {len(df.columns)}")

# Salva uma versão leve para o dashboard
arquivo_saida = "dados_prototipo.csv"

df.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print()
print("Arquivo criado com sucesso!")
print(f"Arquivo: {arquivo_saida}")

# Mostra algumas informações importantes
print()
print("Colunas de origem/destino:")
print([
    col for col in df.columns
    if any(
        palavra in str(col).lower()
        for palavra in ["origem", "destino", "rota", "modal", "uf"]
    )
])

print()
print("Primeiras 5 rotas:")

colunas_rota = [
    "V360[Nome da Origem]",
    "V360[uf_inicial_de_prestacao]",
    "V360[uf_final_de_prestacao]",
    "rota",
    "Modal"
]

print("\n================ COLUNAS IMPORTANTES ================\n")

palavras = [
    "valor",
    "peso",
    "volume",
    "cubagem",
    "custo",
    "entrega",
    "cte",
    "nota",
    "nf"
]

for coluna in df.columns:

    coluna_lower = coluna.lower()

    if any(palavra in coluna_lower for palavra in palavras):
        print(coluna)

print("\n=====================================================\n")


print("\n================ TESTE DE VOLUMES / CAIXAS ================\n")

# Mostra colunas que podem estar relacionadas a quantidade,
# volume, caixa, embalagem ou quantidade de itens.

palavras_volume = [
    "volume",
    "volumes",
    "caixa",
    "caixas",
    "quantidade",
    "qtd",
    "qtde",
    "embalagem",
    "item",
    "unidade"
]

for coluna in df.columns:

    coluna_normalizada = coluna.lower()

    if any(palavra in coluna_normalizada for palavra in palavras_volume):

        print(f"\nCOLUNA: {coluna}")

        print(
            df[coluna]
            .dropna()
            .value_counts()
            .head(10)
            .to_string()
        )

print("\n===========================================================\n")
