import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Dashboard B3", page_icon="📈", layout="wide")

st.title("📈 Analisando os dados da B3")
st.subheader("Luiz Fernando de Jesus")
st.divider()


# criando o upload de arquivos csv na barra lateral (st.sidebar)
arquivo_enviado = st.sidebar.file_uploader(
    label="Envie um arquivo CSV",
    type=["csv"],
    help="Selecione um arquivo com extensão .csv",
)


# Função para carregar os dados com cache
@st.cache_data
def carregar_dados():
    return pd.read_csv(arquivo_enviado)


df_original = carregar_dados()
df = df_original.copy()

# Barra lateral (Sidebar) para filtros
st.sidebar.header("Filtros")
tickers_disponiveis = sorted(df["ticker"].unique())
ticker_selecionado = st.sidebar.selectbox("Selecione o Ticker", tickers_disponiveis)

# Filtrar o DataFrame com base no ticker escolhido
df_filtrado = df[df["ticker"] == ticker_selecionado].sort_values("data")

# Seção de Métricas Principais
st.subheader(f"Visão Geral: {ticker_selecionado}")
col1, col2 = st.columns(2)

with col1:
    ultimo_preco = df_filtrado["preco_fechamento"].iloc[-1]
    st.metric(label="Último Preço de Fechamento", value=f"R$ {ultimo_preco:.2f}")

with col2:
    volume_medio = df_filtrado["volume"].mean()
    st.metric(label="Volume Médio Negociado", value=f"{volume_medio:,.0f}")

# Gráfico de Linha do Preço de Fechamento
st.subheader("Evolução do Preço de Fechamento")
st.line_chart(df_filtrado.set_index("data")["preco_fechamento"])

# Exibir os dados brutos em tabela (opcional)
if st.checkbox("Mostrar tabela de dados filtrados"):
    st.dataframe(df_filtrado)
