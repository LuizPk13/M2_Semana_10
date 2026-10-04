# Bibliotecas
import streamlit as st  # Biblioteca para criar páginas web
import pandas as pd  # Biblioteca para manipular arquivos CSV
import plotly.express as px  # Biblioteca para visualização de gráficos

""""""
st.title("Turma Visualização de Dados - T2")  # Título da minha página.
st.header("Semana Streamlit Básico")  # Cabeçalho da minha página.
st.subheader("Luiz Fernando de Jesus Silva")  # Sub-cabeçalho da minha página.
st.divider()
""""""


""""""  # Configurações da página.
st.set_page_config(
    page_title="Dashboard Financeiro B3",  # Titulo na Aba da Página
    page_icon="📈",  # Ícone na Aba da Página
    layout="wide",  # Layout da Página
    initial_sidebar_state="auto",  # Exibição da barra lateral
)
""""""


""""""  # Configurações do sidebar.
st.sidebar.title("Upload de arquivos")

arquivo_recebido = (
    st.sidebar.file_uploader(  # Levando o upload de arquivos para a barra lateral
        label="Envie um arquivo CSV",  # Título do upload
        type=["csv"],  # Tipos de arquivos que podem ser enviados
        help="Selecione apenas um arquivo com extensão .csv",  # Mensagem de ajuda
    )
)
""""""


""""""
# Abrindo o arquivo enviado.
if arquivo_recebido is not None:
    """"""  # Leitura do arquivo enviado.
    df_original = pd.read_csv(arquivo_recebido)
    df = df_original.copy()  # Cópia do DataFrame original.
    """"""

    """"""  # Configurações do sidebar.
    # Filtros Categoricos
    st.sidebar.title("⚙️ Filtros Categoricos")
    """"""

    """"""  # Definindo as colunas categoricas
    colunas_categoricas = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()  # Lista de colunas categoricas

    if colunas_categoricas:  # Selecionando as colunas categoricas e seus valores.
        coluna_cat = st.sidebar.selectbox(
            label="Escolha a coluna de categoria para filtrar:",
            options=colunas_categoricas,
        )

        opcoes_cat = sorted(df[coluna_cat].dropna().unique())
        categoria_escolhida = st.sidebar.selectbox(
            label=f"Selecione o valor em: {coluna_cat}", options=opcoes_cat
        )

        df = df[df[coluna_cat] == categoria_escolhida]
    """"""

    """"""  # Definindo as colunas numéricas
    colunas_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # Filtros Numericos
    st.sidebar.title("⚙️ Filtros Numericos")

    if colunas_numericas:
        coluna_num = st.sidebar.selectbox(
            label="Escolha a coluna numerica para filtrar:",
            options=colunas_numericas,
        )

        valor_min = float(df[coluna_num].min())
        valor_max = float(df[coluna_num].max())

        # Slide de Intervalo na barra lateral
        if (
            valor_min < valor_max
        ):  # Validação de intervalo, para evitar erros de apenas um unico valor.
            faixa_valores = st.sidebar.slider(
                label=f"Filtre a faixa de valores para: {coluna_num}:",
                min_value=valor_min,
                max_value=valor_max,
                value=(valor_min, valor_max),
                step=0.1 if df[coluna_num].dtype == "float64" else 1.0,
            )
        else:
            st.sidebar.info(
                f"A coluna '{coluna_num}' possui apenas um valor unico: {valor_min}"
            )
            faixa_valores = (valor_min, valor_max)

        # Aplicar os filtros numericos no DataFrame
        df = df[
            (df[coluna_num] >= faixa_valores[0]) & (df[coluna_num] <= faixa_valores[1])
        ]
    """"""

    """"""  # Exibindo as métricas.
    st.subheader("Indicadores")
    col1, col2, col3 = st.columns(3)

    col1.metric("Linhas Filtradas", len(df))
    col2.metric("Total de Registros", len(df_original))
    col3.metric("Total de Colunas", len(df.columns))

    st.divider()
    """"""

    """"""  # Organizando os visuais em abas.
    aba1, aba2 = st.tabs(["tabela filtrada", "resumo estatistico"])

    with aba1:
        st.write(f"Exibindo **`{len(df)}`** de **`{len(df_original)}`** registros:")

    with aba2:
        pass
        st.write("Estatisticas descritivas das colunas numericas:")
        st.dataframe(df.describe(), use_container_width=True)

    # Base bruta completa dentro do expander
    with st.expander("Ver base completa original"):
        pass
        st.dataframe(df_original, use_container_width=True)

    st.divider()
    """"""

    """"""
    if colunas_numericas and not df.empty:
        # Usando o df_original filtrado apenas pelo valor numerico,
        # para que todas as categorias apareçam coloridas no gráfico.
        df_para_grafico = (
            df_original[
                (df_original[coluna_num] >= faixa_valores[0])
                & (df_original[coluna_num] <= faixa_valores[1])
            ]
            if colunas_categoricas
            else df_original
        )

        fig_plotly = px.histogram(
            df_para_grafico,
            x=coluna_num,
            color=(coluna_cat if colunas_categoricas else None),
            title=f"Evolução/Distribuição Interativa de {coluna_num}",
            marginal="box",
        )
        st.plotly_chart(fig_plotly, use_container_width=True)
    else:
        st.info("Nenhuma coluna numerica disponivel para gerar o grafico Plotly.")
    """"""
else:
    st.info("ℹ️ Por favor, faça o upload de um arquivo CSV para visualizar a tabela.")
""""""
