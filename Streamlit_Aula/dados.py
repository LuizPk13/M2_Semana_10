#%%
# import pandas as pd


# df = pd.read_csv("dados_b3_reais.csv")
# df.head()

#%%
import pandas as pd
import yfinance as yf

# Lista ampla de ações tradicionais e líquidas da B3 com longo histórico
tickers = [
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA",
    "ITSA4.SA", "ABEV3.SA", "WEGE3.SA", "CSNA3.SA", "USIM5.SA",
    "GGBR4.SA", "SUZB3.SA", "CMIG4.SA", "EGIE3.SA", "EQTL3.SA",
    "SBSP3.SA", "CSAN3.SA", "VIVT3.SA", "LREN3.SA", "UGPA3.SA",
    "B3SA3.SA"
]

print(f"Baixando histórico de {len(tickers)} ativos da B3 (period='max')...")
# Baixar o histórico completo agrupado por ticker
dados = yf.download(tickers, period="max", group_by="ticker", auto_adjust=False)

# Tratar e organizar a base para formato longo (tidy format)
lista_dfs = []
for t in tickers:
    if t in dados.columns.levels[0]:
        df_ticker = dados[t][["Close", "Volume"]].dropna(subset=["Close"]).copy()
        df_ticker["ticker"] = t.replace(".SA", "")
        df_ticker = df_ticker.reset_index()
        df_ticker.columns = ["data", "preco_fechamento", "volume", "ticker"]
        # Formatar a data para YYYY-MM-DD
        df_ticker["data"] = pd.to_datetime(df_ticker["data"]).dt.strftime("%Y-%m-%d")
        lista_dfs.append(df_ticker)

df_b3_real = pd.concat(lista_dfs, ignore_index=True)

# Salvar em CSV limpo
df_b3_real.to_csv("dados_b3_reais.csv", index=False)
print(f"Base real gerada com sucesso! Total de registros: {len(df_b3_real):,} linhas.")
