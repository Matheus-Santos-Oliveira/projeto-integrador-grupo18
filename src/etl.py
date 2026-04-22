import pandas as pd
import numpy as np

# Carregando o arquivo
df = pd.read_csv('projeto-integrador-grupo18/data/spotify_user_behavior_realistic_50000_rows.csv')

print(df.describe())

# =========================
# CONVERSÃO DE DATA
# =========================
df["signup_date"] = pd.to_datetime(df["signup_date"])  # converte string → datetime para análise temporal

# =========================
# CONVERSÃO DE BOOLEANOS (Yes/No → True/False)
# =========================
df["ad_interaction"] = df["ad_interaction"].str.lower().map({"yes": True, "no": False})  
#transforma interação com anúncio em variável booleana

df["ad_conversion_to_subscription"] = df["ad_conversion_to_subscription"].str.lower().map({"yes": True, "no": False})  
#transforma conversão de anúncio em assinatura em variável booleana

# =========================
# CONVERSÃO DE CATEGÓRICOS
# =========================
cat_cols = [
    "country",
    "subscription_type",
    "subscription_status",
    "favorite_genre",
    "most_liked_feature",
    "desired_future_feature",
    "primary_device"
]

for col in cat_cols:
    df[col] = df[col].astype("category")  
    #otimiza colunas com valores repetidos (economia de memória e melhor agrupamento)

# =========================
# VERIFICAÇÕES FINAIS
# =========================
print(df.dtypes)   # mostra tipos finais após conversão
print(df.describe())  # estatísticas dos dados numéricos