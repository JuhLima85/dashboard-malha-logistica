import streamlit as st

import textwrap


import pandas as pd



import plotly.graph_objects as go



import unicodedata



import re



import requests



import base64



import textwrap



from pathlib import Path











# ============================================================



# CONFIGURAÇÃO



# ============================================================







st.set_page_config(



    page_title="Dashboard de Malha Logística",



    page_icon="🚚",



    layout="wide"



)











# ============================================================

# CSS

# ============================================================

st.markdown(

    """

    <style>

    /* ========================================================

       CARDS DO RESUMO

       ======================================================== */







    .resumo-container {



        display: grid;



        grid-template-columns: repeat(4, minmax(0, 1fr));



        gap: 16px;



        width: 100%;



        margin-top: 10px;



        margin-bottom: 10px;



    }







    .resumo-card {



        background: #171a21;



        border: 1px solid #242832;



        border-radius: 12px;



        padding: 18px 16px;



        min-height: 105px;



        box-sizing: border-box;



        overflow: hidden;



    }







    .resumo-label {



        font-size: 15px;



        font-weight: 600;



        color: #d8d8d8;



        margin-bottom: 14px;



        white-space: nowrap;



    }







    .resumo-valor {



        font-size: 20px;



        font-weight: 700;



        color: #ffffff;



        white-space: nowrap;



        overflow: hidden;



        text-overflow: ellipsis;



    }











    /* ========================================================



       RESPONSIVIDADE



       ======================================================== */







    @media (max-width: 1100px) {







        .resumo-container {



            grid-template-columns: repeat(2, minmax(0, 1fr));



        }







    }











    @media (max-width: 700px) {







        .resumo-container {



            grid-template-columns: repeat(2, minmax(0, 1fr));



        }







    }











    @media (max-width: 450px) {







        .resumo-container {



            grid-template-columns: 1fr;



        }







    }











    /* ========================================================



       MÉTRICAS NATIVAS DO STREAMLIT



       ======================================================== */


div[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.03);
    padding: 5px 10px !important;
    border-radius: 8px;
    min-height: 62px !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 11px !important;
}

div[data-testid="stMetricValue"] {
    font-size: 18px !important;
}



    /* ========================================================



       VISUAL - REFERÊNCIA DARK LOGÍSTICA



       ======================================================== */







    [data-testid="stAppViewContainer"] {



        background: #071522 !important;



    }







    [data-testid="stHeader"] {



        background: rgba(0,0,0,0) !important;



    }







    [data-testid="stSidebar"] {



        background: #081625 !important;



        border-right: 1px solid #10283d;



    }







    [data-testid="stSidebar"] > div:first-child {



        padding-top: 0.7rem;



    }



/* ========================================================
   CABEÇALHO - LOGO + INDICADORES
   ======================================================== */

.header-dashboard {
    display: grid !important;
    grid-template-columns: 1.25fr repeat(4, minmax(0, 1fr)) !important;
    gap: 10px !important;
    width: 100% !important;
    margin: 0 0 14px 0 !important;
    align-items: stretch !important;
}

.header-brand {
    background: #081a2b;
    border: 1px solid #123a5a;
    border-radius: 10px;
    min-width: 0;
    height: 92px;
    padding: 8px 14px;
    box-sizing: border-box;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: hidden;
}

.header-brand img {
    display: block;
    width: 100%;
    max-width: 230px;
    max-height: 72px;
    object-fit: contain;
}

.header-kpi {
    background: #0b1b2c;
    border: 1px solid #123a5a;
    border-radius: 10px;
    min-width: 0;
    height: 92px;
    padding: 12px 14px;
    box-sizing: border-box;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

.header-kpi-label {
    color: #7ea2bf;
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 9px;
    white-space: nowrap;
}

.header-kpi-value {
    color: #f4f9ff;
    font-size: 17px;
    font-weight: 800;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* =====================================================
   CARDS - TOTAL DO DETALHAMENTO
   ===================================================== */

.detalhe-kpis {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 18px;
    width: 100%;
    margin-top: 12px;
    margin-bottom: 20px;
}

.detalhe-kpi {
    background: #0b1b2c;
    border: 1px solid #123a5a;
    border-radius: 10px;
    min-width: 0;
    height: 92px;
    padding: 12px 14px;
    box-sizing: border-box;

    display: flex;
    flex-direction: column;
    justify-content: center;

    overflow: hidden;
}

.detalhe-kpi-label {
    color: #7ea2bf;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 9px;
    white-space: nowrap;
}

/* =====================================================
   CARDS - TOTAL DO DETALHAMENTO
   ===================================================== */

.detalhe-kpi-value {
    color: #f4f9ff;
    font-size: 20px;
    font-weight: 800;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    cursor: default;
}

@media (max-width: 1100px) {
    .header-dashboard {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }
    .header-brand {
        grid-column: 1 / -1;
    }
}

@media (max-width: 650px) {
    .header-dashboard {
        grid-template-columns: 1fr !important;
    }
    .header-brand {
        grid-column: auto;
    }
}

/* ========================================================

   RESPONSIVIDADE

   ======================================================== */







    .section-title {



        color: #eaf5ff;



        font-size: 15px;



        font-weight: 700;



        margin: 4px 0 8px 0;



    }







    .sidebar-section-title {



        color: #dcecff;



        font-size: 14px;



        font-weight: 700;



        margin: 0 0 10px 0;



    }







    .sidebar-kpi {



        background: #0b1b2c;



        border: 1px solid #122d44;



        border-radius: 7px;



        padding: 8px 10px;



        margin: 6px 0;



    }







    .sidebar-kpi-label {



        color: #7ea2bf;



        font-size: 10px;



        margin-bottom: 2px;



    }







    .sidebar-kpi-value {



        color: #f4f9ff;



        font-size: 16px;



        font-weight: 700;



    }







    div[data-testid="stPlotlyChart"] {



        background: #091829 !important;



        border: 1px solid #173650;



        border-radius: 7px;



        padding: 3px;



        box-sizing: border-box;



        box-shadow: inset 0 0 25px rgba(0, 113, 190, 0.06);



    }







    [data-testid="stDataFrame"] {



        border: 1px solid #173650 !important;



        border-radius: 7px !important;



        overflow: hidden !important;



    }







    [data-testid="stDataFrame"] > div {



        background: #091829 !important;



    }







    .resumo-container {



        gap: 8px;



        margin-top: 4px;



    }







    .resumo-card {



        background: #0b1b2c;



        border: 1px solid #122d44;



        border-radius: 7px;



        padding: 9px 11px;



        min-height: 68px;



    }







    .resumo-label {



        font-size: 10px;



        color: #7ea2bf;



        margin-bottom: 6px;



    }







    .resumo-valor {



        font-size: 15px;



        color: #f4f9ff;



    }







    [data-testid="stSidebar"] [data-baseweb="select"] > div {



        background-color: #07111d !important;



        border-color: #173650 !important;



        border-radius: 6px !important;



    }







    [data-testid="stSidebar"] label {



        color: #a9bfd1 !important;



        font-size: 11px !important;



    }







    [data-testid="stSidebar"] [data-baseweb="select"] span {



        color: #dcecff !important;



        font-size: 11px !important;



    }







    [data-testid="stSidebar"] .stMultiSelect {



        margin-bottom: 5px;



    }







    h1, h2, h3 {



        color: #eaf5ff !important;



    }







    .block-container {



        padding-top: 0.65rem !important;



        padding-bottom: 1rem !important;



    }







    </style>



    """,



    unsafe_allow_html=True



)











# ============================================================



# FUNÇÕES



# ============================================================







def normalizar_texto(valor):







    if pd.isna(valor):



        return ""







    texto = str(valor).upper().strip()







    texto = unicodedata.normalize(



        "NFKD",



        texto



    )







    texto = "".join(



        c



        for c in texto



        if not unicodedata.combining(c)



    )







    texto = re.sub(



        r"[^A-Z0-9 ]",



        " ",



        texto



    )







    texto = re.sub(



        r"\s+",



        " ",



        texto



    )







    return texto.strip()











def converter_numerico(serie):







    if serie is None:



        return pd.Series(dtype=float)







    if pd.api.types.is_numeric_dtype(serie):







        return pd.to_numeric(



            serie,



            errors="coerce"



        ).fillna(0)







    texto = (



        serie



        .astype(str)



        .str.strip()



    )







    # Trata números no padrão brasileiro:



    # 1.234,56 -> 1234.56



    #



    # E também números no padrão:



    # 1234.56 -> 1234.56







    possui_virgula = texto.str.contains(



        ",",



        regex=False,



        na=False



    )







    texto_com_virgula = texto.copy()







    texto_com_virgula.loc[possui_virgula] = (



        texto_com_virgula.loc[possui_virgula]



        .str.replace(



            ".",



            "",



            regex=False



        )



        .str.replace(



            ",",



            ".",



            regex=False



        )



    )







    return pd.to_numeric(



        texto_com_virgula,



        errors="coerce"



    ).fillna(0)











def cor_modal(modal):



    modal = normalizar_texto(modal)



    # Aéreo = ciano | Rodoviário = amarelo

    # As cores ajudam a diferenciar rapidamente os modais no mapa.

    if modal == "AEREO":

        return "#35D7FF"



    return "#FFD43B"











def encontrar_coluna(df, candidatos):







    mapa = {



        normalizar_texto(coluna): coluna



        for coluna in df.columns



    }







    # --------------------------------------------------------



    # PRIMEIRO: PROCURA EXATA



    # --------------------------------------------------------







    for candidato in candidatos:







        chave = normalizar_texto(candidato)







        if chave in mapa:



            return mapa[chave]







    # --------------------------------------------------------



    # SEGUNDO: PROCURA PARCIAL



    # --------------------------------------------------------







    for coluna in df.columns:







        coluna_norm = normalizar_texto(coluna)







        for candidato in candidatos:







            candidato_norm = normalizar_texto(candidato)







            if candidato_norm in coluna_norm:



                return coluna







    return None











# ============================================================



# INDICADORES



# ============================================================







def calcular_indicadores(df_base):







    # --------------------------------------------------------



    # VALOR NF



    # --------------------------------------------------------







    if "V360[valor_total_da_carga]" in df_base.columns:







        valor_nf = converter_numerico(



            df_base["V360[valor_total_da_carga]"]



        ).sum()







    else:







        valor_nf = 0











    # --------------------------------------------------------



    # PESO



    # --------------------------------------------------------







    if "V360[peso_total]" in df_base.columns:







        peso = converter_numerico(



            df_base["V360[peso_total]"]



        ).sum()







    else:







        peso = 0











    # --------------------------------------------------------



    # CTES



    # --------------------------------------------------------







    if "V360[numero_da_cte]" in df_base.columns:







        ctes = (



            df_base["V360[numero_da_cte]"]



            .replace("", pd.NA)



            .dropna()



            .nunique()



        )







    else:







        ctes = 0











    # --------------------------------------------------------



    # CUSTOS



    # --------------------------------------------------------







    custo_transferencia = 0



    custo_distribuicao = 0







    if "Custo agregado trsnf" in df_base.columns:







        custo_transferencia = converter_numerico(



            df_base["Custo agregado trsnf"]



        ).sum()











    if "Custo agregado Distribui" in df_base.columns:







        custo_distribuicao = converter_numerico(



            df_base["Custo agregado Distribui"]



        ).sum()











    custos = (



        custo_transferencia



        + custo_distribuicao



    )











    return {



        "valor_nf": valor_nf,



        "peso": peso,



        "ctes": ctes,



        "custos": custos



    }











# ============================================================



# FORMATAÇÃO



# ============================================================







def formatar_moeda(valor):

    return (

        f"R$ {valor:,.2f}"



        .replace(",", "X")



        .replace(".", ",")



        .replace("X", ".")

    )

def formatar_numero(valor):

    return (

        f"{valor:,.0f}"

        .replace(",", ".")

    )

def formatar_decimal(valor):

    return (

        f"{valor:,.2f}"

        .replace(",", "X")

        .replace(".", ",")

        .replace("X", ".")

    )

def formatar_peso(valor):
    try:
        valor = float(valor)

        if valor >= 1000:
            toneladas = valor / 1000
            return f"{formatar_decimal(toneladas)} t"

        return f"{formatar_decimal(valor)} kg"

    except (ValueError, TypeError):
        return "0,00 kg"


# ============================================================

# MAPA DO BRASIL

# ============================================================

@st.cache_data

def carregar_mapa_brasil():

    url = (



        "https://raw.githubusercontent.com/"



        "codeforamerica/click_that_hood/"



        "master/public/data/"



        "brazil-states.geojson"



    )







    resposta = requests.get(



        url,



        timeout=30



    )







    resposta.raise_for_status()







    return resposta.json()











# ============================================================



# CARREGAMENTO DOS DADOS



# ============================================================







@st.cache_data



def carregar_dados():







    dados = pd.read_excel(



        "base_completa.xlsx",



        sheet_name="Base",



        header=0



    )







    municipios = pd.read_csv(



        "municipios.csv",



        low_memory=False,



        encoding="utf-8-sig"



    )







    return dados, municipios











dados, municipios = carregar_dados()











# ============================================================



# COLUNAS PRINCIPAIS



# ============================================================







COL_ORIGEM = "V360[municipio_inicial_de_prestacao]"







COL_UF_ORIGEM = "V360[uf_inicial_de_prestacao]"







COL_DESTINO = "V360[municipio_final_de_prestacao]"







COL_UF_DESTINO = "V360[uf_final_de_prestacao]"







COL_MODAL = "Modal"







COL_ROTA = "rota"







COL_EMPRESA = "V360[Empresas.Empresas]"











# ============================================================



# OPERAÇÃO



# ============================================================







COL_OPERACAO = encontrar_coluna(



    dados,



    [



        "Operação",



        "Operacao",



        "V360[operacao]",



        "V360[operação]",



        "tipo_operacao",



        "tipo de operação"



    ]



)











# ============================================================



# LOCALIZAÇÃO



# ============================================================







COL_LOCALIZACAO = encontrar_coluna(



    dados,



    [



        "Localização",



        "Localizacao",



        "tipo_localizacao",



        "tipo de localização"



    ]



)











# ============================================================



# VALIDAÇÃO



# ============================================================







colunas_necessarias = [







    COL_ORIGEM,



    COL_UF_ORIGEM,



    COL_DESTINO,



    COL_UF_DESTINO,



    COL_EMPRESA







]











colunas_faltando = [







    coluna



    for coluna in colunas_necessarias



    if coluna not in dados.columns







]











if colunas_faltando:







    st.error(



        "Algumas colunas obrigatórias não foram encontradas:"



    )







    for coluna in colunas_faltando:







        st.write(



            f"- `{coluna}`"



        )







    st.stop()











# ============================================================



# PREPARAÇÃO DA BASE



# ============================================================







dados = dados.copy()











dados["origem_cidade"] = (



    dados[COL_ORIGEM]



    .fillna("")



    .astype(str)



    .str.strip()



)











dados["origem_uf"] = (



    dados[COL_UF_ORIGEM]



    .fillna("")



    .astype(str)



    .str.upper()



    .str.strip()



)











dados["destino_cidade"] = (



    dados[COL_DESTINO]



    .fillna("")



    .astype(str)



    .str.strip()



)











dados["destino_uf"] = (



    dados[COL_UF_DESTINO]



    .fillna("")



    .astype(str)



    .str.upper()



    .str.strip()



)











dados["origem_norm"] = (



    dados["origem_cidade"]



    .apply(normalizar_texto)



)











dados["destino_norm"] = (



    dados["destino_cidade"]



    .apply(normalizar_texto)



)











dados["origem_uf"] = (



    dados["origem_uf"]



    .apply(normalizar_texto)



)











dados["destino_uf"] = (



    dados["destino_uf"]



    .apply(normalizar_texto)



)











# ============================================================



# EMPRESA



# ============================================================







dados["empresa_filtro"] = (



    dados[COL_EMPRESA]



    .fillna("")



    .astype(str)



    .str.strip()



)











dados["empresa_filtro"] = (



    dados["empresa_filtro"]



    .replace(



        {



            "nan": "",



            "NaN": "",



            "None": "",



            "NONE": ""



        }



    )



)











# ============================================================



# CHAVES



# ============================================================







dados["chave_origem"] = (



    dados["origem_norm"]



    + "|"



    + dados["origem_uf"]



)











dados["chave_destino"] = (



    dados["destino_norm"]



    + "|"



    + dados["destino_uf"]



)











# ============================================================



# MUNICÍPIOS



# ============================================================







municipios = municipios.copy()











municipios["cidade_norm"] = (



    municipios["nome"]



    .apply(normalizar_texto)



)











mapa_uf = {







    11: "RO",



    12: "AC",



    13: "AM",



    14: "RR",



    15: "PA",



    16: "AP",



    17: "TO",







    21: "MA",



    22: "PI",



    23: "CE",



    24: "RN",



    25: "PB",



    26: "PE",



    27: "AL",



    28: "SE",



    29: "BA",







    31: "MG",



    32: "ES",



    33: "RJ",







    35: "SP",







    41: "PR",



    42: "SC",



    43: "RS",







    50: "MS",



    51: "MT",



    52: "GO",



    53: "DF"







}











municipios["uf"] = (



    municipios["codigo_uf"]



    .map(mapa_uf)



)











municipios["chave"] = (



    municipios["cidade_norm"]



    + "|"



    + municipios["uf"].fillna("")



)











# ============================================================



# LOCALIZAÇÃO



# ============================================================







COL_LOCALIZACAO_BASE = "Cap/Inter"











def classificar_localizacao(valor):







    texto = normalizar_texto(valor)







    if texto == "":



        return ""







    # CAPITAL







    if texto in [



        "CAP",



        "CAPITAL",



        "CAPITAIS",



        "CIDADE CAPITAL",



        "CIDADES CAPITAIS"



    ]:



        return "Capital"











    # INTERIOR







    if texto in [



        "INT",



        "INTERIOR"



    ]:



        return "Interior"











    # Tratamento para textos maiores







    if (



        "CAPITAL" in texto



        or texto.startswith("CAP")



    ):



        return "Capital"











    if (



        "INTERIOR" in texto



        or texto.startswith("INT")



    ):



        return "Interior"











    return ""











if COL_LOCALIZACAO_BASE in dados.columns:







    dados["localizacao_filtro"] = (



        dados[COL_LOCALIZACAO_BASE]



        .fillna("")



        .astype(str)



        .apply(classificar_localizacao)



    )











elif COL_LOCALIZACAO is not None:







    dados["localizacao_filtro"] = (



        dados[COL_LOCALIZACAO]



        .fillna("")



        .astype(str)



        .apply(classificar_localizacao)



    )











else:







    dados["localizacao_filtro"] = ""











dados["localizacao_filtro"] = (



    dados["localizacao_filtro"]



    .fillna("")



    .astype(str)



    .str.strip()



)











# ============================================================



# ROTA



# ============================================================







if COL_ROTA in dados.columns:







    dados["rota_filtro"] = (



        dados[COL_ROTA]



        .fillna("")



        .astype(str)



        .str.strip()



    )







else:







    dados["rota_filtro"] = ""











dados["rota_filtro"] = (



    dados["rota_filtro"]



    .replace(



        {



            "nan": "",



            "NaN": "",



            "None": "",



            "NONE": ""



        }



    )



    .fillna("")



    .astype(str)



    .str.strip()



)











# ============================================================



# CRIA ROTA AUTOMATICAMENTE QUANDO NECESSÁRIO



# ============================================================







rotas_vazias = (



    dados["rota_filtro"] == ""



)











dados.loc[



    rotas_vazias,



    "rota_filtro"



] = (







    dados.loc[



        rotas_vazias,



        "origem_cidade"



    ]



    .astype(str)



    .str.strip()







    + " → "







    + dados.loc[



        rotas_vazias,



        "destino_cidade"



    ]



    .astype(str)



    .str.strip()







)











# ============================================================



# FILTROS



# ============================================================







st.sidebar.markdown("<div class=\"sidebar-section-title\">🔎 Filtros</div>", unsafe_allow_html=True)











# ------------------------------------------------------------



# UF ORIGEM



# ------------------------------------------------------------







ufs_origem = sorted(



    [



        x



        for x in dados["origem_uf"]



        .dropna()



        .unique()

        if x != ""

    ]

)

filtro_uf_origem = st.sidebar.multiselect(

    "UF de origem",
    options=ufs_origem,
    placeholder="Todos"
)

# ------------------------------------------------------------
# UF DESTINO
# ------------------------------------------------------------

ufs_destino = sorted(
    [
        x
        for x in dados["destino_uf"]
        .dropna()
        .unique()
        if x != ""
    ]

)

filtro_uf_destino = st.sidebar.multiselect(

    "UF de destino",
   options=ufs_destino,
    placeholder="Todos"

)
# ------------------------------------------------------------
# MODAL
# ------------------------------------------------------------
if COL_MODAL in dados.columns:
    modais = sorted({str(x).strip() for x in dados[COL_MODAL].dropna()
                     if str(x).strip() and str(x).strip().upper() not in ["NAN", "NONE"]})
else:
    modais = []

filtro_modal = st.sidebar.multiselect(
    "Modal", options=modais, default=[], placeholder="Todos", key="filtro_modal"
)

# ------------------------------------------------------------
# TRANSPORTADOR
# ------------------------------------------------------------
COL_TRANSPORTADOR = encontrar_coluna(
    dados, ["V360[transportador]", "Transportador", "transportador"]
)
transportadores = (
    sorted({str(x).strip() for x in dados[COL_TRANSPORTADOR].dropna()
            if str(x).strip() and str(x).strip().upper() not in ["NAN", "NONE"]})
    if COL_TRANSPORTADOR is not None else []
)
filtro_transportador = st.sidebar.multiselect(
    "Transportador", options=transportadores, default=[],
    placeholder="Todos", key="filtro_transportador"
)

# ------------------------------------------------------------
# PARCEIROS
# ------------------------------------------------------------
COL_PARCEIROS = encontrar_coluna(
    dados, ["Parceiros", "Parceiro", "V360[Parceiros]", "V360[parceiros]"]
)
parceiros = (
    sorted({str(x).strip() for x in dados[COL_PARCEIROS].dropna()
            if str(x).strip() and str(x).strip().upper() not in ["NAN", "NONE"]})
    if COL_PARCEIROS is not None else []
)
filtro_parceiros = st.sidebar.multiselect(
    "Parceiros", options=parceiros, default=[],
    placeholder="Todos", key="filtro_parceiros"
)

# ------------------------------------------------------------
# FROTA PRÓPRIA
# ------------------------------------------------------------
COL_FROTA_PROPRIA = encontrar_coluna(
    dados, ["Frota propria", "Frota própria", "Frota Propria",
            "V360[Frota propria]", "V360[Frota própria]"]
)
frotas_proprias = (
    sorted({str(x).strip() for x in dados[COL_FROTA_PROPRIA].dropna()
            if str(x).strip() and str(x).strip().upper() not in ["NAN", "NONE"]})
    if COL_FROTA_PROPRIA is not None else []
)
filtro_frota_propria = st.sidebar.multiselect(
    "Frota própria", options=frotas_proprias, default=[],
    placeholder="Todos", key="filtro_frota_propria"
)

# ------------------------------------------------------------
# AGREGADO
# ------------------------------------------------------------
COL_AGREGADO = encontrar_coluna(
    dados, ["Agregado", "Agregados", "V360[Agregado]", "V360[agregado]"]
)
agregados = (
    sorted({str(x).strip() for x in dados[COL_AGREGADO].dropna()
            if str(x).strip() and str(x).strip().upper() not in ["NAN", "NONE"]})
    if COL_AGREGADO is not None else []
)
filtro_agregado = st.sidebar.multiselect(
    "Agregado", options=agregados, default=[],
    placeholder="Todos", key="filtro_agregado"
)

# ------------------------------------------------------------
# ROTA
# ------------------------------------------------------------

rotas = sorted(

    [

        x

        for x in dados["rota_filtro"]

        .dropna()

        .unique()

        if str(x).strip() != ""

        and str(x).upper() not in [

            "NAN",

            "NONE"

        ]

    ]



)











filtro_rota = st.sidebar.multiselect(



    "Rota",



    options=rotas,



    placeholder="Todos"



)



# ------------------------------------------------------------
# OPERAÇÃO
# ------------------------------------------------------------

if COL_OPERACAO is not None:


    operacoes = sorted(

        [

            str(x)

            for x in dados[COL_OPERACAO]

            .dropna()

            .unique()

            if str(x).strip() != ""

        ]

    )

    filtro_operacao = st.sidebar.multiselect(

        "Operação",

        options=operacoes,

        placeholder="Todos"

    )

else:

    filtro_operacao = []

    st.sidebar.caption(

        "Operação: coluna não encontrada na base."

    )

# ------------------------------------------------------------
# EMPRESA
# ------------------------------------------------------------

empresas = sorted(

    [
        str(x)

        for x in dados["empresa_filtro"]

        .dropna()

        .unique()

        if str(x).strip() != ""

    ]

)

filtro_empresa = st.sidebar.multiselect(

    "Empresa",

    options=empresas,

    placeholder="Todos"

)

# ------------------------------------------------------------
# LOCALIZAÇÃO
# ------------------------------------------------------------

localizacoes = sorted(

    [

        x

        for x in dados["localizacao_filtro"]

        .dropna()

        .unique()

        if str(x).strip() != ""

    ]


)

filtro_localizacao = st.sidebar.multiselect(

    "Localização",

    options=localizacoes,

    placeholder="Todos"

)

# ============================================================



# APLICAÇÃO DOS FILTROS



# ============================================================

df = dados.copy()

# ------------------------------------------------------------
# UF ORIGEM
# ------------------------------------------------------------
if filtro_uf_origem:
    df = df[
        df["origem_uf"].isin(
            filtro_uf_origem

        )

    ]

# ------------------------------------------------------------

# UF DESTINO

# ------------------------------------------------------------

if filtro_uf_destino:

    df = df[

        df["destino_uf"].isin(

            filtro_uf_destino

        )

    ]



# ------------------------------------------------------------

# MODAL

# ------------------------------------------------------------

if filtro_modal:
    df = df[
        df[COL_MODAL]
        .astype(str)
        .isin(filtro_modal)

    ]

# ------------------------------------------------------------
# TRANSPORTADOR
# ------------------------------------------------------------

if filtro_transportador and COL_TRANSPORTADOR is not None:
    df = df[df[COL_TRANSPORTADOR].fillna("").astype(str).str.strip().isin(filtro_transportador)]

# ------------------------------------------------------------
# PARCEIROS
# ------------------------------------------------------------

if filtro_parceiros and COL_PARCEIROS is not None:
    df = df[df[COL_PARCEIROS].fillna("").astype(str).str.strip().isin(filtro_parceiros)]

# ------------------------------------------------------------
# FROTA PRÓPRIA
# ------------------------------------------------------------

if filtro_frota_propria and COL_FROTA_PROPRIA is not None:
    df = df[df[COL_FROTA_PROPRIA].fillna("").astype(str).str.strip().isin(filtro_frota_propria)]

# ------------------------------------------------------------
# AGREGADO
# ------------------------------------------------------------
if filtro_agregado and COL_AGREGADO is not None:
    df = df[df[COL_AGREGADO].fillna("").astype(str).str.strip().isin(filtro_agregado)]

# ------------------------------------------------------------
# ROTA
# ------------------------------------------------------------

if filtro_rota:

    df = df[

        df["rota_filtro"]

        .astype(str)

        .isin(filtro_rota)

    ]


# ------------------------------------------------------------

# OPERAÇÃO

# ------------------------------------------------------------

if filtro_operacao and COL_OPERACAO is not None:

    df = df[

        df[COL_OPERACAO]

        .astype(str)

        .isin(filtro_operacao)

    ]


# ------------------------------------------------------------

# EMPRESA

# ------------------------------------------------------------

if filtro_empresa:

    df = df[

        df["empresa_filtro"]

        .isin(filtro_empresa)

    ]

# ------------------------------------------------------------

# LOCALIZAÇÃO

# ------------------------------------------------------------

if filtro_localizacao:

    df = df[

        df["localizacao_filtro"]

        .isin(filtro_localizacao)

    ]

# ============================================================

# FILTRO ATIVO

# ============================================================

tem_filtro = (

    bool(filtro_uf_origem)

    or bool(filtro_uf_destino)

    or bool(filtro_modal)

    or bool(filtro_transportador)

    or bool(filtro_parceiros)

    or bool(filtro_frota_propria)

    or bool(filtro_agregado)

    or bool(filtro_rota)

    or bool(filtro_operacao)

    or bool(filtro_empresa)

    or bool(filtro_localizacao)


)

# ============================================================



# INDICADORES LATERAIS



# ============================================================







quantidade_rotas = (



    df[



        [



            "origem_norm",



            "destino_norm"



        ]



    ]



    .drop_duplicates()
    .shape[0]
)

st.sidebar.markdown(
    f"""<div style="margin-top:12px;">
<div class="sidebar-section-title">📊 Indicadores</div>
<div class="sidebar-kpi">
<div class="sidebar-kpi-label">Registros</div>
<div class="sidebar-kpi-value">{len(df):,}</div>
</div>

<div class="sidebar-kpi">
<div class="sidebar-kpi-label">Municípios de origem</div>
<div class="sidebar-kpi-value">{df["origem_norm"].nunique():,}</div>
</div>

<div class="sidebar-kpi">



<div class="sidebar-kpi-label">Municípios de destino</div>



<div class="sidebar-kpi-value">{df["destino_norm"].nunique():,}</div>



</div>







<div class="sidebar-kpi">



<div class="sidebar-kpi-label">Rotas</div>



<div class="sidebar-kpi-value">{quantidade_rotas:,}</div>



</div>



</div>""",



    unsafe_allow_html=True



)











# ============================================================



# MUNICÍPIOS / COORDENADAS



# ============================================================



# ============================================================



# MUNICÍPIOS / COORDENADAS



# ============================================================







municipios_lookup = municipios[



    [



        "chave",



        "nome",



        "uf",



        "latitude",



        "longitude"



    ]



].drop_duplicates("chave")











# ============================================================



# COORDENADAS DE ORIGEM



# ============================================================







df = df.merge(







    municipios_lookup[



        [



            "chave",



            "latitude",



            "longitude"



        ]



    ].rename(



        columns={



            "chave": "chave_origem",



            "latitude": "lat_origem",



            "longitude": "lon_origem"



        }



    ),







    on="chave_origem",







    how="left"







)











# ============================================================



# COORDENADAS DE DESTINO



# ============================================================







df = df.merge(







    municipios_lookup[



        [



            "chave",



            "latitude",



            "longitude"



        ]



    ].rename(



        columns={



            "chave": "chave_destino",



            "latitude": "lat_destino",



            "longitude": "lon_destino"



        }



    ),







    on="chave_destino",







    how="left"







)











# ============================================================



# ROTAS MUNICIPAIS



# ============================================================







rotas_df = (







    df.dropna(



        subset=[



            "lat_origem",



            "lon_origem",



            "lat_destino",



            "lon_destino"



        ]



    )







    .groupby(



        [



            "origem_cidade",



            "origem_uf",



            "destino_cidade",



            "destino_uf",



            "lat_origem",



            "lon_origem",



            "lat_destino",



            "lon_destino",



            COL_MODAL,



            COL_EMPRESA



        ],



        dropna=False



    )







    .size()







    .reset_index(



        name="volume"



    )







    .sort_values(



        "volume",



        ascending=False



    )







)











# ============================================================



# COORDENADAS UFs



# ============================================================







coordenadas_uf = {







    "AC": (-9.9754, -67.8249),



    "AL": (-9.6498, -35.7089),



    "AP": (0.0349, -51.0694),



    "AM": (-3.1190, -60.0217),



    "BA": (-12.9714, -38.5014),



    "CE": (-3.7319, -38.5267),



    "DF": (-15.7975, -47.8919),



    "ES": (-20.3155, -40.3128),



    "GO": (-16.6869, -49.2648),



    "MA": (-2.5307, -44.3068),



    "MT": (-15.6014, -56.0979),



    "MS": (-20.4697, -54.6201),



    "MG": (-19.9167, -43.9345),



    "PA": (-1.4558, -48.4902),



    "PB": (-7.1195, -34.8450),



    "PR": (-25.4284, -49.2733),



    "PE": (-8.0476, -34.8770),



    "PI": (-5.0892, -42.8016),



    "RJ": (-22.9068, -43.1729),



    "RN": (-5.7945, -35.2110),



    "RS": (-30.0346, -51.2177),



    "RO": (-8.7619, -63.9039),



    "RR": (2.8235, -60.6758),



    "SC": (-27.5954, -48.5480),



    "SP": (-23.5505, -46.6333),



    "SE": (-10.9472, -37.0731),



    "TO": (-10.2491, -48.3243)
}

# ============================================================

# ROTAS UF → UF

# ============================================================

# ============================================================
# DADOS NUMÉRICOS PARA O TOOLTIP DAS ROTAS
# ============================================================

df["_valor_nf_mapa"] = converter_numerico(
    df["V360[valor_total_da_carga]"]
)

df["_peso_mapa"] = converter_numerico(
    df["V360[peso_total]"]
)

df["_volumetria_mapa"] = converter_numerico(
    df["V360[peso_cubado]"]
)

df["_custo_transf_mapa"] = converter_numerico(
    df["Custo agregado trsnf"]
)

df["_custo_distrib_mapa"] = converter_numerico(
    df["Custo agregado Distribui"]
)

df["_custo_frota_mapa"] = converter_numerico(
    df["Custo Frota Própria"]
)

df["_custo_mapa"] = (
    df["_custo_transf_mapa"]
    + df["_custo_distrib_mapa"]
    + df["_custo_frota_mapa"]
)


# ============================================================
# ROTAS UF → UF
# ============================================================

rotas_uf = (
    df[
        (df["origem_uf"] != "")
        &
        (df["destino_uf"] != "")
    ]
    .groupby(
        [
            "origem_uf",
            "destino_uf"
        ],
        dropna=False
    )
    .agg(
        volume=(
            "origem_uf",
            "size"
        ),

        Quant_NFs=(
            "V360[chave_de_acesso_nota]",
            lambda x: (
                x.replace("", pd.NA)
                .dropna()
                .nunique()
            )
        ),

        Valor_NF=(
            "_valor_nf_mapa",
            "sum"
        ),

        Peso=(
            "_peso_mapa",
            "sum"
        ),

        Volumetria=(
            "_volumetria_mapa",
            "sum"
        ),

        Custo=(
            "_custo_mapa",
            "sum"
        ),

        Modal=(
            COL_MODAL,
            lambda x: " + ".join(
                sorted(
                    {
                        str(v).strip()
                        for v in x.dropna()
                        if str(v).strip() != ""
                    }
                )
            )
        )
    )
    .reset_index()
    .sort_values(
        "volume",
        ascending=False
    )
)


rotas_uf = rotas_uf[

    rotas_uf["origem_uf"].isin(coordenadas_uf)

    &

    rotas_uf["destino_uf"].isin(coordenadas_uf)

]

rotas_mapa = rotas_uf.copy()

# ============================================================

# COORDENADAS DAS ROTAS

# ============================================================

rotas_mapa["lat_origem"] = (



    rotas_mapa["origem_uf"]



    .map(



        lambda uf:



        coordenadas_uf[uf][0]



    )



)


rotas_mapa["lon_origem"] = (



    rotas_mapa["origem_uf"]



    .map(



        lambda uf:



        coordenadas_uf[uf][1]



    )



)


rotas_mapa["lat_destino"] = (



    rotas_mapa["destino_uf"]



    .map(



        lambda uf:



        coordenadas_uf[uf][0]



    )



)

rotas_mapa["lon_destino"] = (



    rotas_mapa["destino_uf"]



    .map(



        lambda uf:



        coordenadas_uf[uf][1]



    )



)


# ============================================================

# CABEÇALHO - LOGO + INDICADORES

# ============================================================



_pasta_dashboard = Path(__file__).resolve().parent



# Nova logo que colocamos na pasta do projeto

logo_path = _pasta_dashboard / "healthlog_logo.png"



logo_html = ""



if logo_path.exists():



    logo_bytes = logo_path.read_bytes()



    logo_base64 = base64.b64encode(

        logo_bytes

    ).decode("utf-8")



    logo_html = (

        f'<img src="data:image/png;base64,{logo_base64}" '

        f'alt="HealthLog">'

    )



else:



    logo_html = (

        '<span style="color:#eaf5ff;'

        'font-size:22px;'

        'font-weight:800;">'

        'HealthLog'

        '</span>'

    )





# ============================================================

# INDICADORES

# ============================================================



indicadores = calcular_indicadores(df)



valor_nf_formatado = formatar_moeda(

    indicadores["valor_nf"]

)



peso_formatado = (

    formatar_decimal(

        indicadores["peso"]

    )

    + " kg"

)



ctes_formatado = formatar_numero(

    indicadores["ctes"]

)



custos_formatado = formatar_moeda(

    indicadores["custos"]

)





# ============================================================

# CABEÇALHO VISUAL

# ============================================================



header_html = (

    f'<div class="header-dashboard">'



    f'<div class="header-brand">'

    f'{logo_html}'

    f'</div>'



    f'<div class="header-kpi">'

    f'<div class="header-kpi-label">💵 Valor NF</div>'

    f'<div class="header-kpi-value" title="{valor_nf_formatado}">'

    f'{valor_nf_formatado}'

    f'</div>'

    f'</div>'



    f'<div class="header-kpi">'

    f'<div class="header-kpi-label">⚖️ Peso Transportado</div>'

    f'<div class="header-kpi-value" title="{peso_formatado}">'

    f'{peso_formatado}'

    f'</div>'

    f'</div>'



    f'<div class="header-kpi">'

    f'<div class="header-kpi-label">📄 CTEs Emitidos</div>'

    f'<div class="header-kpi-value" title="{ctes_formatado}">'

    f'{ctes_formatado}'

    f'</div>'

    f'</div>'



    f'<div class="header-kpi">'

    f'<div class="header-kpi-label">💰 Custos Logísticos</div>'

    f'<div class="header-kpi-value" title="{custos_formatado}">'

    f'{custos_formatado}'

    f'</div>'

    f'</div>'



    f'</div>'

)



st.markdown(

    header_html,

    unsafe_allow_html=True

)











# ============================================================



# MAPA + HUBS



# ============================================================







col_mapa, col_hubs = st.columns(



    [2.7, 1]



)











# ============================================================



# MAPA



# ============================================================







with col_mapa:







    st.markdown(



        '<div class="section-title">🗺️ Principais Rotas</div>',



        unsafe_allow_html=True



    )











    fig = go.Figure()











    brasil_geojson = (



        carregar_mapa_brasil()



    )











    nomes_estados = [







        feature["properties"]["name"]







        for feature



        in brasil_geojson["features"]







    ]

    # --------------------------------------------------------

    # ESTADOS - MAPA DE CALOR EM 5 TONS DE AZUL

    # --------------------------------------------------------
    # Conta as movimentações em que cada UF participa como origem

    # ou destino. Os valores respeitam todos os filtros selecionados.


        # Valor da NF e Custo Logístico por UF
    valor_nf_por_uf = {}
    custo_por_uf = {}

    for uf in coordenadas_uf:

        mascara_uf = (
            (df["origem_uf"] == uf)
            |
            (df["destino_uf"] == uf)
        )

        # Valor total das Notas Fiscais da UF
        valor_nf_por_uf[uf] = float(
            df.loc[mascara_uf, "_valor_nf_mapa"].sum()
        )

        # Custo Logístico:
        # transferência + distribuição + frota própria
        custo_por_uf[uf] = float(
            df.loc[mascara_uf, "_custo_mapa"].sum()
        )


    # Nome completo dos estados usado pelo GeoJSON

    nome_estado_para_uf = {

        "Acre": "AC",

        "Alagoas": "AL",

        "Amapá": "AP",

        "Amazonas": "AM",

        "Bahia": "BA",

        "Ceará": "CE",

        "Distrito Federal": "DF",

        "Espírito Santo": "ES",

        "Goiás": "GO",

        "Maranhão": "MA",

        "Mato Grosso": "MT",

        "Mato Grosso do Sul": "MS",

        "Minas Gerais": "MG",

        "Pará": "PA",

        "Paraíba": "PB",

        "Paraná": "PR",

        "Pernambuco": "PE",

        "Piauí": "PI",

        "Rio de Janeiro": "RJ",

        "Rio Grande do Norte": "RN",

        "Rio Grande do Sul": "RS",

        "Rondônia": "RO",

        "Roraima": "RR",

        "Santa Catarina": "SC",

        "São Paulo": "SP",

        "Sergipe": "SE",

        "Tocantins": "TO",

    }


        # --------------------------------------------------------
    # NÍVEIS DO VALOR DA NF E DO CUSTO LOGÍSTICO
    # --------------------------------------------------------

    serie_valor_nf = pd.Series(
        valor_nf_por_uf,
        dtype="float64"
    )

    serie_custo = pd.Series(
        custo_por_uf,
        dtype="float64"
    )

    # Cinco níveis para o Valor da NF
    if serie_valor_nf.max() > 0:

        percentuais_valor_nf = (
            serie_valor_nf
            .rank(method="min", pct=True)
        )

        nivel_valor_nf_por_uf = (
            (percentuais_valor_nf * 5)
            .apply(
                lambda x: max(
                    1,
                    min(5, int(x + 0.999999))
                )
            )
            .astype(int)
            .to_dict()
        )

    else:
        nivel_valor_nf_por_uf = {
            uf: 1
            for uf in coordenadas_uf
        }


    # Cinco níveis para o Custo Logístico
    if serie_custo.max() > 0:

        percentuais_custo = (
            serie_custo
            .rank(method="min", pct=True)
        )

        nivel_custo_por_uf = (
            (percentuais_custo * 5)
            .apply(
                lambda x: max(
                    1,
                    min(5, int(x + 0.999999))
                )
            )
            .astype(int)
            .to_dict()
        )

    else:
        nivel_custo_por_uf = {
            uf: 1
            for uf in coordenadas_uf
        }


    # Níveis usados para pintar os estados pelo Valor da NF
    niveis_estados = [
        nivel_valor_nf_por_uf.get(
            nome_estado_para_uf.get(nome_estado, ""),
            1
        )
        for nome_estado in nomes_estados
    ]







    # Azul claro -> azul muito escuro



    tons_azul = [



        "#48B9FF",



        "#2297E8",



        "#1473C2",



        "#0D4F8D",



        "#082F58",



    ]







    # Verde claro -> verde escuro para o custo logístico.
    tons_custo = [
        "#B8EEEE",
        "#7DDDDD",
        "#45CCCC",
        "#22BEBE",
        "#0B7F7F",
    ]

    # Escala discreta: cada estado recebe exatamente um dos 5 tons.



    escala_azul = [



        [0.00, tons_azul[0]],



        [0.1999, tons_azul[0]],



        [0.20, tons_azul[1]],



        [0.3999, tons_azul[1]],



        [0.40, tons_azul[2]],



        [0.5999, tons_azul[2]],



        [0.60, tons_azul[3]],



        [0.7999, tons_azul[3]],



        [0.80, tons_azul[4]],



        [1.00, tons_azul[4]],



    ]

    textos_estados = []

    # Monta primeiro os textos de hover de todos os estados.
    for nome_estado in nomes_estados:
        uf = nome_estado_para_uf.get(nome_estado, "")
        valor_nf_uf = valor_nf_por_uf.get(uf, 0)
        custo_uf = custo_por_uf.get(uf, 0)

        textos_estados.append(
            f"<b>{uf}</b><br>"
            f"{nome_estado}<br><br>"
            f"<b>Valor da NF:</b> {formatar_moeda(valor_nf_uf)}<br>"
            f"<b>Custo Logístico:</b> {formatar_moeda(custo_uf)}"
        )

    # Adiciona o mapa do Brasil apenas uma vez.
    fig.add_trace(
        go.Choropleth(
            geojson=brasil_geojson,
            locations=nomes_estados,
            z=niveis_estados,
            featureidkey="properties.name",
            zmin=1,
            zmax=5,
            colorscale=escala_azul,
            showscale=False,
            marker=dict(
                line=dict(
                    color="#73C9FF",
                    width=1.15
                )
            ),
            text=textos_estados,
            hovertemplate="%{text}<extra></extra>",
            showlegend=False
        )
    )

    # --------------------------------------------------------

    # ROTAS + ÍCONES ANIMADOS

    # --------------------------------------------------------



    # Todas as principais rotas continuam sendo desenhadas.

    # Para não poluir o mapa, os veículos aparecem somente nas

    # rotas de maior volume. Eles percorrem a curva ao iniciar

    # a animação.

    rotas_animadas = []

    MAX_ROTAS_COM_ICONE = 12

        # Verifica se algum filtro está selecionado.
    filtro_espessura_ativo = (
        bool(filtro_uf_origem)
        or bool(filtro_uf_destino)
        or bool(filtro_modal)
        or bool(filtro_transportador)
        or bool(filtro_parceiros)
        or bool(filtro_frota_propria)
        or bool(filtro_agregado)
    )

    for indice_rota, (_, rota) in enumerate(rotas_mapa.iterrows()):



        uf_origem = rota["origem_uf"]

        uf_destino = rota["destino_uf"]



        lat1 = rota["lat_origem"]

        lon1 = rota["lon_origem"]

        lat2 = rota["lat_destino"]

        lon2 = rota["lon_destino"]



        modal = str(rota["Modal"])

        modal_normalizado = normalizar_texto(modal)

        if "AEREO" in modal_normalizado and "RODOVIARIO" in modal_normalizado:
            cor = "#FFFFFF"
        else:
            cor = cor_modal(modal)

        volume = int(rota["volume"])

                # Define a espessura da rota.
        # Sem filtro: mantém a espessura normal.
        # Com filtro: aumenta conforme o Valor da NF.
        if filtro_espessura_ativo and len(rotas_mapa) > 0:

            valor_nf_rota = float(rota["Valor_NF"])

            maior_valor_nf = float(rotas_mapa["Valor_NF"].max())

            if maior_valor_nf > 0:
                proporcao_nf = valor_nf_rota / maior_valor_nf
                espessura_rota = 1.5 + (proporcao_nf * 6.5)
            else:
                espessura_rota = 2.2

        else:
            espessura_rota = 2.2 if indice_rota < MAX_ROTAS_COM_ICONE else 1.5



        if uf_origem == uf_destino:

            continue



        # Mais pontos = movimento mais suave.

        pontos_curva = 48

        t_curva = pd.Series(

            [i / (pontos_curva - 1) for i in range(pontos_curva)]

        )



        dx = lon2 - lon1

        dy = lat2 - lat1

        comprimento = max((dx ** 2 + dy ** 2) ** 0.5, 0.01)



        intensidade_curva = min(

            7.0,

            max(1.5, comprimento * 0.18)

        )



        controle_lon = (

            (lon1 + lon2) / 2

            - (dy / comprimento) * intensidade_curva

        )



        controle_lat = (

            (lat1 + lat2) / 2

            + (dx / comprimento) * intensidade_curva

        )



        lons_curva = (

            (1 - t_curva) ** 2 * lon1

            + 2 * (1 - t_curva) * t_curva * controle_lon

            + t_curva ** 2 * lon2

        )



        lats_curva = (

            (1 - t_curva) ** 2 * lat1

            + 2 * (1 - t_curva) * t_curva * controle_lat

            + t_curva ** 2 * lat2

        )



        # Linha da rota.

        fig.add_trace(

            go.Scattergeo(

                lon=lons_curva.tolist(),

                lat=lats_curva.tolist(),

                mode="lines",

                line=dict(

                    width=espessura_rota,

                    color=cor

                ),

                opacity=0.92 if indice_rota < MAX_ROTAS_COM_ICONE else 0.48,

                hoverinfo="text",

                text=(
                    f"<b>{uf_origem} → {uf_destino}</b><br>"
                    f"Modal: {modal}<br>"
                    f"Quant. de NFs: {int(rota['Quant_NFs']):,}<br>"
                    f"Valor de NF: {formatar_moeda(rota['Valor_NF'])}<br>"
                   f"Peso: {formatar_peso(rota['Peso'])}<br>"
                    f"Volumetria: {formatar_decimal(rota['Volumetria'])}<br>"
                    f"Custo: {formatar_moeda(rota['Custo'])}"
                ),

                showlegend=False

            )

        )

                    # Ponta triangular da seta apontando para o destino
        if len(lons_curva) >= 6 and len(lats_curva) >= 6:

            # A ponta fica um pouco antes do marcador do destino
            indice_ponta = -2

            lon_ponta = lons_curva.iloc[indice_ponta]
            lat_ponta = lats_curva.iloc[indice_ponta]

            # Ponto anterior usado para descobrir a direção da rota
            lon_anterior = lons_curva.iloc[-6]
            lat_anterior = lats_curva.iloc[-6]

            dx_seta = lon_ponta - lon_anterior
            dy_seta = lat_ponta - lat_anterior

            comprimento = max(
                (dx_seta ** 2 + dy_seta ** 2) ** 0.5,
                0.0001
            )

            # Vetor da direção da rota
            dir_lon = dx_seta / comprimento
            dir_lat = dy_seta / comprimento

            # Vetor perpendicular
            perp_lon = -dir_lat
            perp_lat = dir_lon

            # Tamanho da ponta acompanha a espessura da rota
            comprimento_ponta = 0.18 + (espessura_rota * 0.020)
            largura_ponta = 0.10 + (espessura_rota * 0.012)

            # Centro da base do triângulo
            base_lon = lon_ponta - dir_lon * comprimento_ponta
            base_lat = lat_ponta - dir_lat * comprimento_ponta

            # Dois lados da base
            ponta1_lon = base_lon + perp_lon * largura_ponta
            ponta1_lat = base_lat + perp_lat * largura_ponta

            ponta2_lon = base_lon - perp_lon * largura_ponta
            ponta2_lat = base_lat - perp_lat * largura_ponta

            # Triângulo preenchido
            fig.add_trace(
                go.Scattergeo(
                    lon=[
                        ponta1_lon,
                        lon_ponta,
                        ponta2_lon,
                        ponta1_lon
                    ],
                    lat=[
                        ponta1_lat,
                        lat_ponta,
                        ponta2_lat,
                        ponta1_lat
                    ],
                    mode="lines",
                    fill="toself",
                    fillcolor="#FF4B4B",
                    line=dict(
                        color="#FF4B4B",
                        width=1
                    ),
                    hoverinfo="skip",
                    showlegend=False
                )
            )



        # Mostra veículo apenas nas principais rotas, evitando

        # sobreposição de muitos ícones ao mesmo tempo.

        if indice_rota >= MAX_ROTAS_COM_ICONE:

            continue



        if "AEREO" in modal_normalizado and "RODOVIARIO" in modal_normalizado:

            icone_modal = "✈️🚚"

            tamanho_icone = 20

        elif "AEREO" in modal_normalizado:

            icone_modal = "✈️"

            tamanho_icone = 22

        else:

            icone_modal = "🚚"

            tamanho_icone = 21



        # Os veículos começam em posições diferentes da rota.

        indice_inicial = (indice_rota * 7) % pontos_curva



        fig.add_trace(

            go.Scattergeo(

                lon=[lons_curva.iloc[indice_inicial]],

                lat=[lats_curva.iloc[indice_inicial]],

                mode="text",

                text=[icone_modal],

                textfont=dict(size=tamanho_icone),

                hoverinfo="text",

                hovertext=(

                    f"<b>{icone_modal} {uf_origem} → {uf_destino}</b><br>"

                    f"Modal: {modal}<br>"

                    f"Movimentações: {volume:,}"

                ),

                showlegend=False

            )

        )





        indice_trace_icone = len(fig.data) - 1



        rotas_animadas.append(

            {

                "trace": indice_trace_icone,

                "lons": lons_curva.tolist(),

                "lats": lats_curva.tolist(),

                "icone": icone_modal,

                "tamanho": tamanho_icone,

                "offset": indice_rota * 7,

            }

        )



    # --------------------------------------------------------

    # ANIMAÇÃO DOS CAMINHÕES E AVIÕES

    # --------------------------------------------------------



    if rotas_animadas:

        total_frames = 48

        frames = []



        for numero_frame in range(total_frames):

            dados_frame = []

            traces_frame = []



            for rota_animada in rotas_animadas:

                quantidade_pontos = len(rota_animada["lons"])

                posicao = (

                    numero_frame + rota_animada["offset"]

                ) % quantidade_pontos



                dados_frame.append(

                    go.Scattergeo(

                        lon=[rota_animada["lons"][posicao]],

                        lat=[rota_animada["lats"][posicao]],

                        mode="text",

                        text=[rota_animada["icone"]],

                        textfont=dict(size=rota_animada["tamanho"]),

                        hoverinfo="skip",

                        showlegend=False

                    )

                )



                traces_frame.append(rota_animada["trace"])



            frames.append(

                go.Frame(

                    data=dados_frame,

                    traces=traces_frame,

                    name=str(numero_frame)

                )

            )



        fig.frames = frames

    # --------------------------------------------------------

    # SIGLAS DAS UFs

    # --------------------------------------------------------

    ufs_mapa = set()

    lat_ufs = []

    lon_ufs = []

    nomes_ufs = []

    textos_ufs = []

    niveis_custo_ufs = []

    for _, rota in rotas_mapa.iterrows():

        ufs_mapa.add(rota["origem_uf"])

        ufs_mapa.add(rota["destino_uf"])

    for uf in sorted(ufs_mapa):

        lat, lon = coordenadas_uf[uf]

        valor_nf_uf = valor_nf_por_uf.get(uf, 0)
        custo_uf = custo_por_uf.get(uf, 0)
        nivel_custo_uf = nivel_custo_por_uf.get(uf, 1)

        texto = (
        f"<b>UF: {uf}</b><br><br>"
        f"<b>Valor da NF:</b> {formatar_moeda(valor_nf_uf)}<br>"
        f"<b>Custo Logístico:</b> {formatar_moeda(custo_uf)}"
    )   

        lat_ufs.append(lat)

        lon_ufs.append(lon)

        nomes_ufs.append(uf)

        textos_ufs.append(texto)

        niveis_custo_ufs.append(nivel_custo_uf)

    if len(lat_ufs) > 0:

        fig.add_trace(

            go.Scattergeo(

                lat=lat_ufs,

                lon=lon_ufs,

                mode="markers+text",

                text=nomes_ufs,

                textposition="top center",

                textfont=dict(

                    size=10,

                    color="white"

                ),

                marker=dict(
                    size=[
                        7 + (nivel * 3)
                        for nivel in niveis_custo_ufs
                    ],
                    color=[
                        tons_custo[nivel - 1]
                        for nivel in niveis_custo_ufs
                    ],
                    opacity=0.85,
                    line=dict(
                        width=1,
                        color="#FFFFFF"
                    )
                ),

                hoverinfo="text",

                hovertext=textos_ufs,

                showlegend=False

            )

        )

    # --------------------------------------------------------
        # --------------------------------------------------------
# LEGENDA - VALOR DA NF
# --------------------------------------------------------

fig.add_annotation(
    x=0.92,
    y=0.105,
    xref="paper",
    yref="paper",
    text="<b>Valor da NF</b>",
    showarrow=False,
    font=dict(
        size=11,
        color="white"
    ),
    xanchor="right",
    yanchor="bottom"
)

# --------------------------------------------------------
# LEGENDA - CUSTO LOGÍSTICO
# --------------------------------------------------------

fig.add_annotation(
    x=0.92,
    y=0.035,
    xref="paper",
    yref="paper",
    text="<b>Custo Logístico</b>",
    showarrow=False,
    font=dict(
        size=11,
        color="white"
    ),
    xanchor="right",
    yanchor="bottom"
)



largura_caixa = 0.035
espacamento = 0.006
inicio_x = 0.72


# --------------------------------------------------------
# 5 NÍVEIS - VALOR DA NF
# --------------------------------------------------------

y_valor_nf = 0.080

for indice, cor in enumerate(tons_azul):

    x0 = inicio_x + indice * (
        largura_caixa + espacamento
    )

    x1 = x0 + largura_caixa

    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=x0,
        x1=x1,
        y0=y_valor_nf,
        y1=y_valor_nf + 0.022,
        fillcolor=cor,
        line=dict(
            color=cor,
            width=1
        )
    )

    fig.add_annotation(
        x=(x0 + x1) / 2,
        y=y_valor_nf - 0.008,
        xref="paper",
        yref="paper",
        text=str(indice + 1),
        showarrow=False,
        font=dict(
            size=8,
            color="#BFC7D5"
        ),
        xanchor="center",
        yanchor="top"
    )


# --------------------------------------------------------
# 5 NÍVEIS - CUSTO LOGÍSTICO
# --------------------------------------------------------

y_custo = 0.010

for indice, cor in enumerate(tons_custo):

    x0 = inicio_x + indice * (
        largura_caixa + espacamento
    )

    x1 = x0 + largura_caixa

    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=x0,
        x1=x1,
        y0=y_custo,
        y1=y_custo + 0.022,
        fillcolor=cor,
        line=dict(
            color=cor,
            width=1
        )
    )

    fig.add_annotation(
        x=(x0 + x1) / 2,
        y=y_custo - 0.008,
        xref="paper",
        yref="paper",
        text=str(indice + 1),
        showarrow=False,
        font=dict(
            size=8,
            color="#BFC7D5"
        ),
        xanchor="center",
        yanchor="top"
    )







with col_mapa:

    # Legenda dos modais



    fig.add_trace(



        go.Scattergeo(



            lon=[None],



            lat=[None],



            mode="lines",



            line=dict(



                color="#FFD43B",



                width=3



            ),



            name="🚚 Rodoviário",



            showlegend=True



        )



    )







    fig.add_trace(



        go.Scattergeo(



            lon=[None],



            lat=[None],



            mode="lines",



            line=dict(



                color="#35D7FF",



                width=3



            ),



            name="✈️ Aéreo",



            showlegend=True



        )



    )







    # --------------------------------------------------------



    # CONFIGURAÇÃO DO MAPA



    # --------------------------------------------------------







    fig.update_geos(

        scope="south america",

        showland=False,

        showcountries=False,

        showcoastlines=False,

        showlakes=False,

        showrivers=False,

        showframe=False,

        bgcolor="#0B1829",

        projection=dict(

            type="mercator"

        ),

        center=dict(

            lat=-14,

            lon=-52

        ),

        lonaxis=dict(

            range=[-74, -34]

        ),

        lataxis=dict(

            range=[-34, 6]

        ),

        fitbounds=False

    )







    # --------------------------------------------------------



    # LAYOUT



    # --------------------------------------------------------







    fig.update_layout(



        height=560,



        margin=dict(



            l=0,



            r=0,



            t=0,



            b=0



        ),



        paper_bgcolor="#0B1829",



        plot_bgcolor="#0B1829",



        showlegend=True,



        legend=dict(



            orientation="h",



            x=0.035,



            y=0.055,



            xanchor="left",



            yanchor="bottom",



            bgcolor="rgba(10, 24, 40, 0.82)",



            bordercolor="rgba(255,255,255,0.12)",



            borderwidth=1,



            font=dict(



                size=10,



                color="white"



            )



        ),



        # Botões para iniciar e pausar o movimento dos veículos.

        updatemenus=[



            dict(



                type="buttons",



                direction="left",



                showactive=False,



                x=0.50,



                y=0.955,



                xanchor="center",



                yanchor="top",



                bgcolor="rgba(10, 24, 40, 0.85)",



                bordercolor="rgba(255,255,255,0.15)",



                borderwidth=1,



                buttons=[



                    dict(



                        label="▶ Rotas em movimento",



                        method="animate",



                        args=[



                            None,



                            {



                                "frame": {



                                    "duration": 180,



                                    "redraw": False



                                },



                                "transition": {



                                    "duration": 0



                                },



                                "fromcurrent": True,



                                "mode": "immediate"



                            }



                        ]



                    ),



                    dict(



                        label="⏸ Pausar",



                        method="animate",



                        args=[



                            [None],



                            {



                                "frame": {



                                    "duration": 0,



                                    "redraw": False



                                },



                                "transition": {



                                    "duration": 0



                                },



                                "mode": "immediate"



                            }



                        ]



                    )



                ]



            )



        ]



    )







    st.plotly_chart(



        fig,



        use_container_width=True,



        config={



            "displayModeBar": False



        }



    )











# ============================================================



# PRINCIPAIS HUBS



# ============================================================







with col_hubs:







    st.markdown(



        '<div class="section-title">🏭 Principais Hubs</div>',



        unsafe_allow_html=True



    )











    hubs = (







        df[



            df["origem_cidade"]



            .str.strip()



            != ""



        ]







        .groupby(



            [



                "origem_cidade",



                "origem_uf"



            ]



        )







        .size()







        .reset_index(



            name="movimentacoes"



        )

        .sort_values(



            "movimentacoes",



            ascending=False



        )

        .head(50)


    )











    hubs["Hub"] = (







        hubs["origem_cidade"]







        + " - "







        + hubs["origem_uf"]







    )











    hubs_exibicao = (







        hubs[



            [



                "Hub",



                "movimentacoes"



            ]



        ]







        .rename(



            columns={



                "movimentacoes":



                "Movimentações"



            }



        )

    )

    if len(hubs_exibicao) > 0:

        st.dataframe(

            hubs_exibicao,

            use_container_width=True,

            height=445,

            hide_index=True
        )

    else:

        st.info(

            "Nenhum hub encontrado."

        )


# ============================================================
# DETALHAMENTO DAS ROTAS
# ============================================================

st.subheader("📊 Detalhamento das principais rotas")

COL_NF = "V360[chave_de_acesso_nota]"
COL_VALOR_NF = "V360[valor_total_da_carga]"
COL_PESO = "V360[peso_total]"
COL_VOLUMETRIA = "V360[peso_cubado]"
COL_CUSTO_TRANSF = "Custo agregado trsnf"
COL_CUSTO_DISTRIB = "Custo agregado Distribui"
COL_CUSTO_FROTA = "Custo Frota Própria"

if len(df) > 0:

    # --------------------------------------------------------
    # BASE PARA O DETALHAMENTO
    # --------------------------------------------------------

    detalhe = df.copy()

    # Converte valores para numérico
    detalhe["_valor_nf"] = converter_numerico(
        detalhe[COL_VALOR_NF]
    )

    detalhe["_peso"] = converter_numerico(
        detalhe[COL_PESO]
    )

    detalhe["_volumetria"] = converter_numerico(
        detalhe[COL_VOLUMETRIA]
    )

    detalhe["_custo_transf"] = converter_numerico(
        detalhe[COL_CUSTO_TRANSF]
    )

    detalhe["_custo_distrib"] = converter_numerico(
        detalhe[COL_CUSTO_DISTRIB]
    )

    detalhe["_custo_frota"] = converter_numerico(
        detalhe[COL_CUSTO_FROTA]
    )

    detalhe["_custo"] = (
        detalhe["_custo_transf"]
        + detalhe["_custo_distrib"]
        + detalhe["_custo_frota"]
    )

    # --------------------------------------------------------
    # AGRUPAMENTO POR ORIGEM E DESTINO
    # --------------------------------------------------------

    tabela_rotas = (
        detalhe
        .groupby(
            [
                "origem_cidade",
                "origem_uf",
                "destino_cidade",
                "destino_uf",
                 COL_MODAL
            ],
            dropna=False
        )
        .agg(
            Quant_NFs=(
                COL_NF,
                lambda x: x.replace("", pd.NA)
                           .dropna()
                           .nunique()
            ),
           Valor_NF=("_valor_nf", "sum"),
            Peso=("_peso", "sum"),
            Volumetria=("_volumetria", "sum"),
            Custo=("_custo", "sum")
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # ORIGEM E DESTINO
    # --------------------------------------------------------

    tabela_rotas["Origem"] = (
        tabela_rotas["origem_cidade"].astype(str)
        + " - "
        + tabela_rotas["origem_uf"].astype(str)
    )

    tabela_rotas["Destino"] = (
        tabela_rotas["destino_cidade"].astype(str)
        + " - "
        + tabela_rotas["destino_uf"].astype(str)
    )

    # --------------------------------------------------------
    # ORDENAÇÃO
    # --------------------------------------------------------

    tabela_rotas = tabela_rotas.sort_values(
        "Valor_NF",
        ascending=False
    )

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    total_nfs = (
        detalhe[COL_NF]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )

    total_valor_nf = detalhe["_valor_nf"].sum()
    total_peso = detalhe["_peso"].sum()
    total_volumetria = detalhe["_volumetria"].sum()
    total_custo = detalhe["_custo"].sum()

    # --------------------------------------------------------
    # TABELA PARA EXIBIÇÃO
    # --------------------------------------------------------

    tabela_exibicao = tabela_rotas[
        [
            "Origem",
            "Destino",
            "Quant_NFs",
            "Valor_NF",
            "Peso",
            "Volumetria",
            "Custo",
            COL_MODAL
        ]
    ].copy()

    tabela_exibicao = tabela_exibicao.rename(
        columns={
            "Quant_NFs": "Quant. de NFs",
            "Valor_NF": "Valor de NF",
            "Peso": "Peso",
            "Volumetria": "Volumetria",
             "Custo": "Custo",
             COL_MODAL: "Modal"
        }
    )

    tabela_exibicao["Quant. Modal"] = tabela_exibicao["Quant. de NFs"]

        # Formata Valor de NF no padrão brasileiro
    tabela_exibicao["Valor de NF"] = (
        tabela_exibicao["Valor de NF"]
        .apply(formatar_moeda)
    )

    # Formata Custo no padrão brasileiro
    tabela_exibicao["Custo"] = (
        tabela_exibicao["Custo"]
        .apply(formatar_moeda)
    )

    # --------------------------------------------------------
    # MOSTRA DETALHAMENTO
    # --------------------------------------------------------

    tabela_exibicao["Peso"] = tabela_exibicao["Peso"].apply(formatar_peso)

    st.dataframe(
        tabela_exibicao,
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            "Quant. de NFs": st.column_config.NumberColumn(
                "Quant. de NFs",
                format="%d"
            ),
            
            "Peso": st.column_config.TextColumn(
              "Peso"
            ),
            "Volumetria": st.column_config.NumberColumn(
                "Volumetria",
                format="%.2f"
            ),
            "Custo": st.column_config.TextColumn(
               "Custo"
            ),
            "Modal": st.column_config.TextColumn(
               "Modal"
            ),
            "Quant. Modal": st.column_config.NumberColumn(
               "Quant. Modal",
               format="%d"
            )
        }
    )

    total_modal = (
        detalhe[COL_MODAL]
        .replace("", pd.NA)
        .dropna()
        .count()
    )

    # --------------------------------------------------------
    # TOTAL DO DETALHAMENTO
    # --------------------------------------------------------

    st.markdown("#### Total do detalhamento")

    # Formata os valores
    total_nfs_formatado = formatar_numero(total_nfs)
    total_valor_formatado = formatar_moeda(total_valor_nf)
    total_peso_formatado = formatar_peso(total_peso)
    total_vol_formatado = formatar_decimal(total_volumetria)
    total_custo_formatado = formatar_moeda(total_custo)
    total_modal_formatado = formatar_numero(total_modal)

    st.html(
    f"""
    <div class="detalhe-kpis">

        <div class="detalhe-kpi">
            <div class="detalhe-kpi-label">Quant. de NFs</div>
            <div class="detalhe-kpi-value" title="{total_nfs_formatado}">
                {total_nfs_formatado}
            </div>
        </div>

        <div class="detalhe-kpi">
            <div class="detalhe-kpi-label">Valor de NF</div>
            <div class="detalhe-kpi-value" title="{total_valor_formatado}">
                {total_valor_formatado}
            </div>
        </div>

        <div class="detalhe-kpi">
            <div class="detalhe-kpi-label">Peso</div>
            <div class="detalhe-kpi-value" title="{total_peso_formatado}">
                {total_peso_formatado}
            </div>
        </div>

        <div class="detalhe-kpi">
            <div class="detalhe-kpi-label">Volumetria</div>
            <div class="detalhe-kpi-value" title="{total_vol_formatado}">
                {total_vol_formatado}
            </div>
        </div>

        <div class="detalhe-kpi">
            <div class="detalhe-kpi-label">Custo</div>
            <div class="detalhe-kpi-value" title="{total_custo_formatado}">
                {total_custo_formatado}
            </div>
        </div>

        <div class="detalhe-kpi">
            <div class="detalhe-kpi-label">Quant. Modal</div>
            <div class="detalhe-kpi-value" title="{total_modal_formatado}">
                {total_modal_formatado}
            </div>
        </div>

        </div>
    """,
    
    )

else:

     st.info(
            "Nenhuma rota encontrada "
            "com os filtros selecionados."
            )
