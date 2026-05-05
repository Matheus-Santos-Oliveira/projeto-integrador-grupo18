"""
Projeto Integrador – Grupo 18
Semana 3: Transformações e Enriquecimento dos Dados
Responsável: Murilo de Oliveira Santos

Entregáveis:
  ✅ Novas colunas: age_group, user_type, ad_group
  ✅ Métricas derivadas: avg_listening, top funções desejadas, satisfação média
  ✅ Agrupamentos e agregações prontos para o dashboard
  ✅ Export: spotify_enriched.csv
"""

import pandas as pd
import numpy as np

# ══════════════════════════════════════════════════════════════════════
# 1. CARREGAMENTO
# ══════════════════════════════════════════════════════════════════════
FILE_PATH = "../data/spotify_user_behavior_realistic_50000_rows.csv"
df = pd.read_csv(FILE_PATH)
print(f"✅ Dataset carregado: {df.shape[0]:,} linhas × {df.shape[1]} colunas\n")


# ══════════════════════════════════════════════════════════════════════
# 2. CONVERSÃO DE TIPOS (complemento às semanas 1 e 2)
# ══════════════════════════════════════════════════════════════════════
df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")

cols_cat = [
    "country", "subscription_type", "subscription_status",
    "favorite_genre", "most_liked_feature",
    "desired_future_feature", "primary_device",
]
for col in cols_cat:
    df[col] = df[col].astype("category")

# Yes/No → booleano
for col in ["ad_interaction", "ad_conversion_to_subscription"]:
    df[col] = df[col].str.strip().str.lower().map({"yes": True, "no": False})


# ══════════════════════════════════════════════════════════════════════
# 3. NOVAS COLUNAS DERIVADAS
# ══════════════════════════════════════════════════════════════════════

# ── 3.1 Faixa etária ──────────────────────────────────────────────────
bins   = [0,  17,  24,  34,  44,  54, 200]
labels = ["< 18", "18–24", "25–34", "35–44", "45–54", "55+"]

df["age_group"] = pd.cut(
    df["age"], bins=bins, labels=labels, right=True
)

print("📊 Distribuição por faixa etária:")
print(df["age_group"].value_counts().sort_index().to_string())
print()

# ── 3.2 Tipo de usuário: Heavy / Casual ───────────────────────────────
# Critério: >= mediana de horas semanais → Heavy
listening_median = df["avg_listening_hours_per_week"].median()

df["user_type"] = pd.Categorical(np.where(
    df["avg_listening_hours_per_week"] >= listening_median,
    "Heavy",
    "Casual"
))

print(f"📊 Mediana de horas/semana usada como corte: {listening_median:.2f} h")
print(df["user_type"].value_counts().to_string())
print()

# ── 3.3 Grupo de anúncio ──────────────────────────────────────────────
# Categorias:
#   "Sem Anúncio"         → não viu anúncio
#   "Anúncio → Converteu" → viu anúncio e assinou
#   "Anúncio → Não Conv." → viu anúncio mas não assinou

def classify_ad_group(row):
    if not row["ad_interaction"]:
        return "Sem Anúncio"
    elif row["ad_conversion_to_subscription"]:
        return "Anúncio → Converteu"
    else:
        return "Anúncio → Não Conv."

df["ad_group"] = df.apply(classify_ad_group, axis=1).astype("category")

print("📊 Grupos de anúncio:")
print(df["ad_group"].value_counts().to_string())
print()


# ══════════════════════════════════════════════════════════════════════
# 4. MÉTRICAS DERIVADAS (escalares)
# ══════════════════════════════════════════════════════════════════════

# ── 4.1 Média de tempo de escuta ─────────────────────────────────────
avg_listening = df["avg_listening_hours_per_week"].mean()
print(f"🎵 Média de horas de escuta/semana (geral): {avg_listening:.2f} h")

# Por tipo de assinatura
listening_by_plan = (
    df.groupby("subscription_type", observed=True)["avg_listening_hours_per_week"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
    .rename("avg_hours_per_week")
)
print("\n🎵 Média de escuta por plano:")
print(listening_by_plan.to_string())
print()

# ── 4.2 Funções mais desejadas ────────────────────────────────────────
top_desired = (
    df["desired_future_feature"]
    .value_counts()
    .rename_axis("feature")
    .reset_index(name="count")
)
top_desired["pct"] = (top_desired["count"] / len(df) * 100).round(2)

print("🔧 Funções mais desejadas:")
print(top_desired.to_string(index=False))
print()

# ── 4.3 Satisfação média ─────────────────────────────────────────────
avg_satisfaction = df["music_suggestion_rating_1_to_5"].mean()
print(f"⭐ Satisfação média (1–5): {avg_satisfaction:.2f}")

# Por plano
satisfaction_by_plan = (
    df.groupby("subscription_type", observed=True)["music_suggestion_rating_1_to_5"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
    .rename("avg_rating")
)
print("\n⭐ Satisfação média por plano:")
print(satisfaction_by_plan.to_string())
print()


# ══════════════════════════════════════════════════════════════════════
# 5. AGRUPAMENTOS E AGREGAÇÕES (tabelas para o dashboard)
# ══════════════════════════════════════════════════════════════════════

# ── 5.1 KPIs gerais ───────────────────────────────────────────────────
total_users         = len(df)
pct_premium         = (df["subscription_type"] != "Free").mean() * 100
pct_ad_interaction  = df["ad_interaction"].mean() * 100
pct_ad_conversion   = (
    df[df["ad_interaction"]]["ad_conversion_to_subscription"].mean() * 100
)
avg_skips           = df["avg_skips_per_day"].mean()
avg_playlists       = df["playlists_created"].mean()

kpis = pd.DataFrame({
    "metric": [
        "Total de usuários",
        "% com plano pago",
        "% interagiram com anúncio",
        "% conversão via anúncio (dentre quem viu)",
        "Média de skips/dia",
        "Média de playlists criadas",
        "Satisfação média (1–5)",
        "Horas de escuta/semana",
    ],
    "value": [
        f"{total_users:,}",
        f"{pct_premium:.1f}%",
        f"{pct_ad_interaction:.1f}%",
        f"{pct_ad_conversion:.1f}%",
        f"{avg_skips:.2f}",
        f"{avg_playlists:.2f}",
        f"{avg_satisfaction:.2f}",
        f"{avg_listening:.2f} h",
    ]
})
print("📋 KPIs Gerais:")
print(kpis.to_string(index=False))
print()

# ── 5.2 Engajamento por faixa etária e tipo de usuário ────────────────
engagement_by_age = (
    df.groupby(["age_group", "user_type"], observed=True)
    .agg(
        total_users       = ("user_id", "count"),
        avg_hours         = ("avg_listening_hours_per_week", "mean"),
        avg_rating        = ("music_suggestion_rating_1_to_5", "mean"),
        avg_skips         = ("avg_skips_per_day", "mean"),
        avg_playlists     = ("playlists_created", "mean"),
    )
    .round(2)
    .reset_index()
)

# ── 5.3 Conversão premium por grupo de anúncio ────────────────────────
conversion_by_ad = (
    df.groupby("ad_group", observed=True)
    .agg(
        total              = ("user_id", "count"),
        premium_count      = ("subscription_type", lambda x: (x != "Free").sum()),
        avg_satisfaction   = ("music_suggestion_rating_1_to_5", "mean"),
        avg_hours          = ("avg_listening_hours_per_week", "mean"),
    )
    .round(2)
    .reset_index()
)
conversion_by_ad["pct_premium"] = (
    conversion_by_ad["premium_count"] / conversion_by_ad["total"] * 100
).round(2)

# ── 5.4 Gêneros mais ouvidos ──────────────────────────────────────────
genre_counts = (
    df["favorite_genre"]
    .value_counts()
    .rename_axis("genre")
    .reset_index(name="count")
)
genre_counts["pct"] = (genre_counts["count"] / len(df) * 100).round(2)

# ── 5.5 Funcionalidades mais curtidas ─────────────────────────────────
liked_features = (
    df["most_liked_feature"]
    .value_counts()
    .rename_axis("feature")
    .reset_index(name="count")
)
liked_features["pct"] = (liked_features["count"] / len(df) * 100).round(2)

# ── 5.6 Relação skips × satisfação (por faixa) ────────────────────────
max_skips = int(df["avg_skips_per_day"].max())

df["skip_group"] = pd.cut(
    df["avg_skips_per_day"],
    bins=[0, 3, 6, 10, 16, max_skips],
    labels=[
        "Baixo (0–3)",
        "Médio (4–6)",
        "Alto (7–10)",
        "Muito alto (11–16)",
        f"Extremo (17–{max_skips})",
    ],
    right=True
)
skip_vs_satisfaction = (
    df.groupby("skip_group", observed=True)["music_suggestion_rating_1_to_5"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "avg_rating", "count": "users"})
    .round(2)
    .reset_index()
)

# ── 5.7 Dispositivo × tipo de usuário ─────────────────────────────────
device_user_type = (
    df.groupby(["primary_device", "user_type"], observed=True)
    .agg(
        count    = ("user_id", "count"),
        avg_hours = ("avg_listening_hours_per_week", "mean"),
    )
    .round(2)
    .reset_index()
)

print("✅ Todos os agrupamentos calculados.\n")


# ══════════════════════════════════════════════════════════════════════
# 6. EXPORTAÇÃO
# ══════════════════════════════════════════════════════════════════════
OUTPUT_ENRICHED   = "../data/spotify_enriched.csv"
OUTPUT_KPI        = "../data/agg_kpis.csv"
OUTPUT_GENRE      = "../data/agg_genres.csv"
OUTPUT_FEATURES   = "../data/agg_desired_features.csv"
OUTPUT_LIKED      = "../data/agg_liked_features.csv"
OUTPUT_AD         = "../data/agg_ad_conversion.csv"
OUTPUT_AGE        = "../data/agg_engagement_by_age.csv"
OUTPUT_SKIP       = "../data/agg_skip_satisfaction.csv"
OUTPUT_DEVICE     = "../data/agg_device_user_type.csv"

df.to_csv(OUTPUT_ENRICHED, index=False)
kpis.to_csv(OUTPUT_KPI, index=False)
genre_counts.to_csv(OUTPUT_GENRE, index=False)
top_desired.to_csv(OUTPUT_FEATURES, index=False)
liked_features.to_csv(OUTPUT_LIKED, index=False)
conversion_by_ad.to_csv(OUTPUT_AD, index=False)
engagement_by_age.to_csv(OUTPUT_AGE, index=False)
skip_vs_satisfaction.to_csv(OUTPUT_SKIP, index=False)
device_user_type.to_csv(OUTPUT_DEVICE, index=False)

print("📁 Arquivos exportados:")
outputs = [
    (OUTPUT_ENRICHED, "Dataset enriquecido (base principal)"),
    (OUTPUT_KPI,      "KPIs gerais"),
    (OUTPUT_GENRE,    "Gêneros favoritos"),
    (OUTPUT_FEATURES, "Funções desejadas"),
    (OUTPUT_LIKED,    "Funções mais curtidas"),
    (OUTPUT_AD,       "Conversão por grupo de anúncio"),
    (OUTPUT_AGE,      "Engajamento por faixa etária"),
    (OUTPUT_SKIP,     "Skips vs Satisfação"),
    (OUTPUT_DEVICE,   "Dispositivo vs Tipo de usuário"),
]
for fname, desc in outputs:
    print(f"   • {fname:<35} → {desc}")

print("\n✅ Semana 3 concluída com sucesso!")
