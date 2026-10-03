# importando as libs
import streamlit as st
import pandas as pd

# importando função genérica do arquivo functions.py (exemplo em aula)
# from functions import mensagem_boas_vindas


# definindo o titulo da pagina
st.title("Lendo arquivos csv")
st.header("Turma Visualização de Dados - FIESC 2026/2")
st.subheader("Semana Streamlit Básico")

# Exemplo de uso da função externa importada
mensagem_boas_vindas("Turma FIESC")


# criando a liberação de upload de arquivos csv na pagina
arquivo_enviado = st.file_uploader(
    label="Envie um arquivo CSV",
    type=["csv"],
    help="Selecione um arquivo com extensão .csv",
)

# Passo 3, 4 e 5: Ler, filtrar (texto e número) e exibir os dados
if arquivo_enviado is not None:
    # Passo 3: Ler o arquivo com pd.read_csv()
    df = pd.read_csv(arquivo_enviado)

    # DataFrame auxiliar para acumular os filtros
    df_filtrado = df.copy()

    # --- PASSO 4: Filtro por Coluna Categórica (st.selectbox) ---
    colunas_categoricas = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if colunas_categoricas:
        coluna_cat = st.selectbox(
            label="Escolha a coluna de categoria para filtrar:",
            options=colunas_categoricas,
        )

        st.write(f"Coluna Selecionada de Filtro: {coluna_cat}")

        opcoes_cat = sorted(df[coluna_cat].dropna().unique())
        categoria_escolhida = st.selectbox(
            label=f"Selecione o valor em '{coluna_cat}':",
            options=opcoes_cat,
        )

        st.write(f"Coluna Selecionada de Filtro: {categoria_escolhida}")

        df_filtrado = df_filtrado[df_filtrado[coluna_cat] == categoria_escolhida]
    # --- PASSO 5: Filtro por Coluna Numérica (st.slider e st.number_input) ---
    colunas_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if colunas_numericas:
        coluna_num = st.selectbox(
            label="Escolha a coluna numérica para filtrar:",
            options=colunas_numericas,
        )

        val_min = float(df[coluna_num].min())
        val_max = float(df[coluna_num].max())

        # Exemplo A: Slider de Intervalo (st.slider)
        faixa_valores = st.slider(
            label=f"Filtre a faixa de valores para '{coluna_num}' (st.slider):",
            min_value=val_min,
            max_value=val_max,
            value=(val_min, val_max),
            step=0.1 if df[coluna_num].dtype == "float64" else 1.0,
        )

        # Exemplo B: Entrada Numérica para limite mínimo manual (st.number_input)
        limite_minimo = st.number_input(
            label=f"Ou digite o valor mínimo exato para '{coluna_num}' (st.number_input):",
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

    # Exibe a contagem e a tabela final filtrada
    st.write(f"Exibindo **{len(df_filtrado)}** de **{len(df)}** registros:")
    st.dataframe(df_filtrado, use_container_width=True)

    # --------------------------------------------------------------------------
    # 3. COLUNAS PARALELAS (st.columns) E CARTÕES DE MÉTRICAS (st.metric)
    # --------------------------------------------------------------------------
    # st.columns(3) divide a tela horizontalmente em 3 partes iguais
    st.subheader("📌 Indicadores Rápidos (KPIs)")
    col1, col2, col3 = st.columns(3)

    # st.metric cria cartões visuais de destaque para números importantes
    col1.metric(label="Linhas Filtradas", value=len(df_filtrado))
    col2.metric(label="Total Original", value=len(df))
    col3.metric(label="Total de Colunas", value=len(df.columns))

    st.divider()

    # --------------------------------------------------------------------------
    # Exemplo simples de Sidebar (Barra Lateral)
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.header("⚙️ Barra Lateral (st.sidebar)")
        st.write(
            "Tudo colocado dentro deste bloco aparece no menu retrátil à esquerda!"
        )
        st.info(f"Registros filtrados no momento: {len(df_filtrado)}")

        # --------------------------------------------------------------------------
        # 4. NAVEGAÇÃO EM ABAS (st.tabs)
        # --------------------------------------------------------------------------

        # st.tabs permite alternar entre visões diferentes sem rolar a página
        aba1, aba2 = st.tabs(["📋 Tabela Filtrada", "📊 Resumo Estatístico"])

        # Conteúdo que aparece quando o aluno clica na primeira aba
        with aba1:
            st.write(f"Exibindo **{len(df_filtrado)}** de **{len(df)}** registros:")
            st.dataframe(df_filtrado, use_container_width=True)

        # Conteúdo que aparece quando o aluno clica na segunda aba
        with aba2:
            st.write("Estatísticas descritivas (média, mínimo, máximo, etc.):")
            st.dataframe(df_filtrado.describe(), use_container_width=True)

        # Base bruta completa dentro do expander
        with st.expander("Ver base completa original"):
            st.dataframe(df, use_container_width=True)


else:
    st.info("ℹ️ Por favor, faça o upload de um arquivo CSV para visualizar a tabela.")
