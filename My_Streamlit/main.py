import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Meu Streamlit", layout="wide", initial_sidebar_state="auto"
)

# Titulo e Subtitulo da página
st.title("Meu Streamlit")
st.subheader("Luiz Fernando de Jesus")
st.divider()

# Criando um bloco para enviar arquivos na sidebar
arquivo_recebido = st.sidebar.file_uploader(
    label="Envie um arquivo CSV",
    type=["csv"],
    help="Selecione apenas um arquivo com extensão .csv",
)

if arquivo_recebido is not None:

  @st.cache_data  # Guardando a primeira leitura em cache
  def carregar_dados(arquivo):
    return pd.read_csv(arquivo)

  df_original = carregar_dados(arquivo_recebido)
  df = df_original.copy()  # Cópia do dataframe original para filtrar

  st.sidebar.header("Filtros e Configurações")

  # 1. Tratamento das Colunas Categóricas
  colunas_categoricas = df.select_dtypes(
      include=["object", "category"]
  ).columns.tolist()
  colunas_cat = None

  if colunas_categoricas:
    colunas_cat = st.sidebar.selectbox(
        label="Colunas categóricas", options=colunas_categoricas
    )

  # 2. Tratamento das Colunas Numéricas
  colunas_numericas = df.select_dtypes(
      include=["int64", "float64"]
  ).columns.tolist()
  colunas_num = None

  if colunas_numericas:
    colunas_num = st.sidebar.selectbox(
        label="Colunas numéricas", options=colunas_numericas
    )

    # Area de Graficos
    st.subheader("Gerando gráficos")
    st.divider()

    # Tabela
    st.subheader("Tabela Original")
    st.dataframe(df_original, use_container_width=True)
else:
  st.info("Por favor, faça o upload de um arquivo CSV na barra lateral.")