# importando as libs
import streamlit as st
import pandas as pd


# definindo o titulo da pagina
st.title("Lendo arquivos csv")


# criando a liberação de upload de arquivos csv na pagina
arquivo_enviado = st.file_uploader(
        label="Envie um arquivo CSV",
        type=["csv"],
        help='Selecione um arquivo com extensão .csv'
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

        opcoes_cat = sorted(df[coluna_cat].dropna().unique())
        categoria_escolhida = st.selectbox(
            label=f"Selecione o valor em '{coluna_cat}':",
            options=opcoes_cat,
        )

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

else:
    st.info("ℹ️ Por favor, faça o upload de um arquivo CSV para visualizar a tabela.")
