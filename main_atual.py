# importando as libs
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# definindo o titulo da pagina
st.title("Lendo arquivos csv")
st.header("Turma Visualização de Dados - FIESC 2026/2")
st.subheader("Semana Streamlit Básico")

# Configuração da página
st.set_page_config(
    page_title="Dashboard Financeiro B3",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
)

# ==============================================================================
# ITEM 1: Mover filtros e botão de carregar arquivo para a barra lateral (st.sidebar)
# ==============================================================================

# criando o upload de arquivos csv na barra lateral (st.sidebar)
arquivo_enviado = st.sidebar.file_uploader(
    label="Envie um arquivo CSV",
    type=["csv"],
    help="Selecione um arquivo com extensão .csv, POR FAVOR!",
)

# Passo 3, 4 e 5: Ler, filtrar (texto e número) e exibir os dados
if arquivo_enviado is not None:

    @st.cache_data  # guarda o resultado na memória RAM (evita re-leitura a cada clique)
    def carregar_dados(arquivo):  # função para ler os dados do arquivo enviado
        return pd.read_csv(
            arquivo
        )  # lê o arquivo CSV com pandas apenas na primeira execução

    df = carregar_dados(
        arquivo_enviado
    )  # executa a função de leitura protegida pelo cache

    # DataFrame auxiliar para acumular os filtros
    df_filtrado = df.copy()

    # --- PASSO 4: Filtro por Coluna Categórica na barra lateral (st.sidebar.selectbox) ---
    colunas_categoricas = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if colunas_categoricas:
        coluna_cat = st.sidebar.selectbox(
            label="Escolha a coluna de categoria para filtrar:",
            options=colunas_categoricas,
        )

        st.sidebar.write(f"Coluna Selecionada: {coluna_cat}")

        opcoes_cat = sorted(df[coluna_cat].dropna().unique())
        categoria_escolhida = st.sidebar.selectbox(
            label=f"Selecione o valor em '{coluna_cat}':",
            options=opcoes_cat,
        )

        st.sidebar.write(f"Valor Selecionado: {categoria_escolhida}")

        df_filtrado = df_filtrado[df_filtrado[coluna_cat] == categoria_escolhida]

    # --- PASSO 5: Filtro por Coluna Numérica na barra lateral (st.sidebar) ---
    colunas_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if colunas_numericas:
        coluna_num = st.sidebar.selectbox(
            label="Escolha a coluna numérica para filtrar:",
            options=colunas_numericas,
        )

        val_min = float(df[coluna_num].min())
        val_max = float(df[coluna_num].max())

        # Slider de Intervalo na barra lateral
        faixa_valores = st.sidebar.slider(
            label=f"Filtre a faixa de valores para '{coluna_num}':",
            min_value=val_min,
            max_value=val_max,
            value=(val_min, val_max),
            step=0.1 if df[coluna_num].dtype == "float64" else 1.0,
        )

        # Entrada Numérica para limite mínimo na barra lateral
        limite_minimo = st.sidebar.number_input(
            label=f"Ou digite o valor mínimo exato para '{coluna_num}':",
            min_value=val_min,
            max_value=val_max,
            value=val_min,
        )

        # Aplica os filtros numéricos no DataFrame
        df_filtrado = df_filtrado[
            (df_filtrado[coluna_num] >= faixa_valores[0])
            & (df_filtrado[coluna_num] <= faixa_valores[1])
            & (df_filtrado[coluna_num] >= limite_minimo)
        ]

    # ==============================================================================
    # ITEM 2: Criar 3 colunas (st.columns(3)) no topo para exibir cartões de métricas
    # ==============================================================================
    st.subheader("Indicadores")
    col1, col2, col3 = st.columns(3)

    col1.metric("Linhas Filtradas", len(df_filtrado))
    col2.metric("Total de Linhas", len(df))
    col3.metric("Total de Colunas", len(df.columns))

    st.divider()

    # ==============================================================================
    # ITEM 3: Organizar os visuais em abas e colocar a base bruta dentro de um st.expander
    # ==============================================================================
    aba1, aba2 = st.tabs(["Tabela Filtrada", "Resumo Estatístico"])

    with aba1:
        st.write(f"Exibindo **{len(df_filtrado)}** de **{len(df)}** registros:")
        st.dataframe(df_filtrado, use_container_width=True)

    with aba2:
        st.write("Estatísticas descritivas das colunas numéricas:")
        st.dataframe(df_filtrado.describe(), use_container_width=True)

    # Base bruta completa dentro do expander
    with st.expander("Ver base completa original"):
        st.dataframe(df, use_container_width=True)

    st.divider()
    st.header("📊 Aula 03 - Visualizações e Performance")

    # 1. teste plt
    st.subheader("1. Visualização Estática com Matplotlib (st.pyplot)")
    st.caption("Ideal para distribuições de frequência e relatórios estáticos.")

    if colunas_numericas and not df_filtrado.empty:
        fig, ax = plt.subplots(figsize=(8, 4))  # cria a figura (fig) e os eixos (ax)
        ax.hist(  # plota o histograma de frequência
            df_filtrado[coluna_num].dropna(),  # valores da coluna numérica sem nulos
            bins=20,  # quantidade de colunas/faixas do histograma
            color="#2E86C1",  # cor azul das barras
            edgecolor="black",  # borda preta em cada barra
        )
        ax.set_title(f"Distribuição do {coluna_num}")  # título do gráfico
        ax.set_xlabel(f"{coluna_num} (R$)")  # rótulo do eixo horizontal X
        ax.set_ylabel("Frequência")  # rótulo do eixo vertical Y

        st.pyplot(fig)  # renderiza a figura no Streamlit (evita plt.show())
    else:
        st.info("Nenhuma coluna numérica disponível para gerar o gráfico Matplotlib.")

    # 2. teste ploply
    st.subheader("2. Visualização Interativa com Plotly (st.plotly_chart)")
    st.caption("Suporte nativo a hover (detalhes ao passar o mouse), zoom e pan.")

    if colunas_numericas and not df_filtrado.empty:
        fig_plotly = px.histogram(  # cria histograma interativo do Plotly
            df_filtrado,  # dados filtrados
            x=coluna_num,  # coluna no eixo horizontal X
            color=(
                coluna_cat if colunas_categoricas else None
            ),  # divide por cores de categoria se houver
            title=f"Evolução/Distribuição Interativa de {coluna_num}",  # título da visualização
            marginal="box",  # adiciona boxplot no topo do gráfico
        )
        st.plotly_chart(
            fig_plotly, use_container_width=True
        )  # exibe ajustado à largura da tela
    else:
        st.info("Nenhuma coluna numérica disponível para gerar o gráfico Plotly.")

else:
    st.info(
        "ℹ️ Por favor, faça o upload de um arquivo CSV na barra lateral para visualizar a tabela."
    )
