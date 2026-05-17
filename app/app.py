# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Spotify User Behavior",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

GREEN = "#1DB954"
GREEN_SCALE = ["#0a5224", "#0f7a33", "#17a845", GREEN]

TITLE_FONT = dict(size=20, color="#ffffff")

LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#dde1ea", family="sans-serif", size=15),
    xaxis=dict(
        gridcolor="#1c2030",
        linecolor="#2a2d3a",
        tickcolor="#4b5563",
        tickfont=dict(size=14, color="#dde1ea"),
        title_font=dict(size=15, color="#dde1ea"),
    ),
    yaxis=dict(
        gridcolor="#1c2030",
        linecolor="#2a2d3a",
        tickcolor="#4b5563",
        tickfont=dict(size=14, color="#dde1ea"),
        title_font=dict(size=15, color="#dde1ea"),
    ),
    margin=dict(l=10, r=30, t=60, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#dde1ea", size=15)),
)

TEXT_STYLE = dict(
    textfont=dict(color="#ffffff", size=16),
    marker=dict(line=dict(width=0), cornerradius=6),
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

@st.cache_data
def load(filename):
    return pd.read_csv(os.path.join(DATA_DIR, filename), encoding="latin-1")

df_kpis = load("agg_kpis.csv")
df_genres = load("agg_genres.csv")
df_desired = load("agg_desired_features.csv")
df_liked = load("agg_liked_features.csv")
df_ad = load("agg_ad_conversion.csv")
df_age = load("agg_engagement_by_age.csv")
df_skip = load("agg_skip_satisfaction.csv")
df_device = load("agg_device_user_type.csv")

def fix_encoding(df):
    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col]
            .str.encode("latin-1", errors="ignore")
            .str.decode("utf-8", errors="ignore")
        )
    return df

for _df in [df_ad, df_age, df_skip, df_device, df_kpis]:
    fix_encoding(_df)

with st.sidebar:
    st.markdown("## Painel de Controle")
    st.markdown("Escolha quais gráficos exibir:")
    st.markdown("---")

    show_genres = st.checkbox("Gêneros Musicais", value=True, key="cb1")
    show_desired = st.checkbox("Funcionalidades Desejadas", value=True, key="cb2")
    show_liked = st.checkbox("Funcionalidades Apreciadas", value=True, key="cb3")
    show_ad = st.checkbox("Impacto dos Anúncios", value=True, key="cb4")
    show_age = st.checkbox("Engajamento por Idade", value=True, key="cb5")
    show_skip = st.checkbox("Skips x Satisfação", value=True, key="cb6")
    show_device = st.checkbox("Dispositivos", value=True, key="cb7")

    st.markdown("---")
    st.caption("Use os filtros acima para controlar os gráficos exibidos.")

st.markdown("""
<div>
  <div class="dash-title">Spotify User Behavior Dashboard</div>

  <div class="dash-group-line">
    Grupo 18 - João Paulo &nbsp;&middot;&nbsp; Matheus &nbsp;&middot;&nbsp; Murilo
  </div>
</div>

<p class="intro-sub">
Análise de engajamento, satisfação e monetização de usuários da plataforma.
</p>

<div class="dashboard-note">
  <strong>Nota sobre a leitura dos gráficos:</strong>
  alguns gráficos exibem inicialmente apenas as categorias mais relevantes para manter a visualização clara.
  Os percentuais são calculados sobre o total da base de dados; por isso, quando a opção Top 5 ou Top 10 estiver selecionada,
  a soma das barras exibidas pode ser menor que 100%.
</div>
""", unsafe_allow_html=True)

kpi_items = list(zip(df_kpis["metric"], df_kpis["value"]))

def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

kpi_row(kpi_items[:4])

if len(kpi_items) > 4:
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    kpi_row(kpi_items[4:])

st.markdown("<hr>", unsafe_allow_html=True)

if show_genres:
    st.subheader("Gêneros Musicais Favoritos")
    top_n = st.selectbox(
        "Exibir:",
        options=[5, 10, 15, len(df_genres)],
        format_func=lambda x: f"Top {x}" if x != len(df_genres) else "Todos",
        key="sel_genres",
    )

    df_g = df_genres.nlargest(top_n, "count").sort_values("count")

    fig1 = px.bar(
        df_g,
        x="count",
        y="genre",
        orientation="h",
        text=df_g["pct"].apply(lambda x: f"{x:.1f}%"),
        color="count",
        color_continuous_scale=GREEN_SCALE,
        labels={"count": "Quantidade de Usuários", "genre": "Gênero Musical"},
    )

    fig1.update_traces(textposition="outside", **TEXT_STYLE)
    fig1.update_coloraxes(showscale=False)
    fig1.update_layout(**LAYOUT, title=dict(text="Contagem por gênero favorito", font=TITLE_FONT))
    fig1.update_xaxes(title="Quantidade de Usuários")
    fig1.update_yaxes(title="Gênero Musical")

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    <div class="section-desc">
    <strong>Insight:</strong> Os gêneros estão distribuídos de forma relativamente uniforme,
    sem uma preferência dominante isolada. Isso indica uma base diversificada de usuários,
    reforçando a importância de recomendações personalizadas ao invés de playlists genéricas.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

if show_desired:
    st.subheader("Funcionalidades Mais Desejadas pelos Usuários")
    top_d = st.selectbox(
        "Exibir:",
        options=[5, 10, len(df_desired)],
        format_func=lambda x: f"Top {x}" if x != len(df_desired) else "Todas",
        key="sel_desired",
    )

    df_d = df_desired.nlargest(top_d, "count").sort_values("count")

    fig2 = px.bar(
        df_d,
        x="count",
        y="feature",
        orientation="h",
        text=df_d["pct"].apply(lambda x: f"{x:.1f}%"),
        color="count",
        color_continuous_scale=GREEN_SCALE,
        labels={"count": "Quantidade de Usuários", "feature": "Funcionalidade"},
    )

    fig2.update_traces(textposition="outside", **TEXT_STYLE)
    fig2.update_coloraxes(showscale=False)
    fig2.update_layout(**LAYOUT, title=dict(text="Funcionalidades desejadas no futuro", font=TITLE_FONT))
    fig2.update_xaxes(title="Quantidade de Usuários")
    fig2.update_yaxes(title="Funcionalidade")

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="section-desc">
        <strong>Insight:</strong> As funcionalidades desejadas apresentam distribuição bastante equilibrada,
    sem uma preferência dominante isolada. Mood-based Auto Playlists e Concert Alerts
    aparecem entre as mais citadas, indicando interesse tanto em personalização
    quanto em experiências mais interativas e contextuais.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

if show_liked:
    st.subheader("Funcionalidades Mais Apreciadas Atualmente")

    feature_col = [c for c in df_liked.columns if c not in ("count", "pct")][0]

    top_l = st.selectbox(
        "Exibir:",
        options=[5, 10, len(df_liked)],
        format_func=lambda x: f"Top {x}" if x != len(df_liked) else "Todas",
        key="sel_liked",
    )

    df_l = df_liked.nlargest(top_l, "count").sort_values("count")

    fig3 = px.bar(
        df_l,
        x="count",
        y=feature_col,
        orientation="h",
        text=df_l["pct"].apply(lambda x: f"{x:.1f}%") if "pct" in df_l.columns else None,
        color="count",
        color_continuous_scale=GREEN_SCALE,
        labels={"count": "Quantidade de Usuários", feature_col: "Funcionalidade"},
    )

    fig3.update_traces(textposition="outside", **TEXT_STYLE)
    fig3.update_coloraxes(showscale=False)
    fig3.update_layout(**LAYOUT, title=dict(text="Funcionalidades favoritas atuais", font=TITLE_FONT))
    fig3.update_xaxes(title="Quantidade de Usuários")
    fig3.update_yaxes(title="Funcionalidade")

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div class="section-desc">
    <strong>Insight:</strong> As funcionalidades mais apreciadas apresentam distribuição bastante equilibrada,
    sem concentração dominante em um único recurso. Isso indica que diferentes perfis de usuários
    extraem valor de experiências distintas da plataforma, reforçando a importância de manter
    um ecossistema diversificado de funcionalidades ao invés de priorizar apenas um tipo de experiência.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
if show_ad:
    st.subheader("Impacto dos Anúncios na Conversão Premium")

    metric_ad = st.selectbox(
        "Métrica a visualizar:",
        options=[
            "Percentual com Plano Pago",
            "Satisfação Média",
            "Horas de Escuta Médias"
        ],
        key="sel_ad",
    )

    metric_map = {
        "Percentual com Plano Pago": (
            "pct_premium",
            "% de usuários com plano pago"
        ),

        "Satisfação Média": (
            "avg_satisfaction",
            "Satisfação Média (1-5)"
        ),

        "Horas de Escuta Médias": (
            "avg_hours",
            "Horas/Semana"
        ),
    }

    col_name, col_label = metric_map[metric_ad]

    fig4 = px.bar(
        df_ad,
        x="ad_group",
        y=col_name,
        text=df_ad[col_name].apply(lambda x: f"{x:.2f}"),
        color="ad_group",
        color_discrete_sequence=[GREEN, "#17a845", "#0a5224"],
        labels={"ad_group": "Grupo de Anúncio", col_name: col_label},
    )

    fig4.update_traces(textposition="outside", **TEXT_STYLE)
    fig4.update_layout(
        **LAYOUT,
        title=dict(text=f"{col_label} por grupo de anúncio", font=TITLE_FONT),
        showlegend=False,
    )
    fig4.update_yaxes(title=col_label)
    fig4.update_xaxes(title="Grupo de Anúncio")

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
<div class="section-desc">
<strong>Insight:</strong> Os grupos de anúncio apresentam percentuais muito próximos de usuários
com plano pago, além de níveis semelhantes de satisfação e horas médias de escuta. Isso indica
que, nesta base, a interação com anúncios não está associada a diferenças expressivas nas métricas
observadas. Usuários do grupo "Sem Anúncio" também podem possuir plano pago, mas não são classificados
como conversões originadas por anúncio.
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

if show_age:
    st.subheader("Engajamento por Faixa Etária e Tipo de Usuário")

    metric_age = st.selectbox(
        "Métrica de engajamento:",
        options=["Horas de Escuta", "Satisfação Média", "Skips por Dia", "Playlists Criadas"],
        key="sel_age",
    )

    metric_age_map = {
        "Horas de Escuta": ("avg_hours", "Horas/Semana"),
        "Satisfação Média": ("avg_rating", "Satisfação (1-5)"),
        "Skips por Dia": ("avg_skips", "Skips/Dia"),
        "Playlists Criadas": ("avg_playlists", "Playlists"),
    }

    col_age, label_age = metric_age_map[metric_age]

    df_age_pt = df_age.copy()
    df_age_pt["Tipo de Usuario"] = df_age_pt["user_type"].map(
        {"Heavy": "Intenso", "Casual": "Casual"}
    ).fillna(df_age_pt["user_type"])

    fig5 = px.bar(
        df_age_pt,
        x="age_group",
        y=col_age,
        color="Tipo de Usuario",
        barmode="group",
        color_discrete_map={"Intenso": GREEN, "Casual": "#3a4055"},
        text=df_age_pt[col_age].apply(lambda x: f"{x:.1f}"),
        labels={"age_group": "Faixa Etária", col_age: label_age},
    )

    fig5.update_traces(textposition="outside", **TEXT_STYLE)
    fig5.update_layout(
        **LAYOUT,
        title=dict(text=f"{label_age} por faixa etária e tipo de usuário", font=TITLE_FONT),
    )
    fig5.update_yaxes(title=label_age)
    fig5.update_xaxes(title="Faixa Etária")

    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""
    <div class="section-desc">
    <strong>Insight:</strong> Usuários Intensos, acima de 9,98 horas por semana, mantêm engajamento
    consistente em todas as faixas etárias, mostrando que uso intenso não é exclusivo de jovens.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

if show_skip:
    st.subheader("Satisfação por Comportamento de Skips")

    view_skip = st.selectbox(
        "Visualizar por:",
        options=["Satisfação Média", "Total de Usuários"],
        key="sel_skip",
    )

    if view_skip == "Satisfação Média":
        fig6 = px.bar(
            df_skip,
            x="skip_group",
            y="avg_rating",
            text=df_skip["avg_rating"].apply(lambda x: f"{x:.2f}"),
            color="avg_rating",
            color_continuous_scale=GREEN_SCALE,
            labels={"skip_group": "Grupo de Skips", "avg_rating": "Satisfação Média (1-5)"},
        )
        fig6.update_yaxes(title="Satisfação Média (1-5)", range=[0, 5])
    else:
        fig6 = px.bar(
            df_skip,
            x="skip_group",
            y="users",
            text="users",
            color="users",
            color_continuous_scale=GREEN_SCALE,
            labels={"skip_group": "Grupo de Skips", "users": "Número de Usuários"},
        )
        fig6.update_yaxes(title="Número de Usuários")

    fig6.update_traces(textposition="outside", **TEXT_STYLE)
    fig6.update_coloraxes(showscale=False)
    fig6.update_layout(**LAYOUT, title=dict(text="Satisfação vs. comportamento de skips", font=TITLE_FONT))
    fig6.update_xaxes(title="Grupo de Skips")

    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
    <div class="section-desc">
    <strong>Insight:</strong> Os níveis de satisfação permaneceram bastante estáveis entre os diferentes
    grupos de comportamento de skips, variando entre 3,62 e 3,65. Isso sugere que, nesta base,
    o número de músicas puladas não apresentou relação expressiva com a satisfação geral dos usuários,
    indicando que outros fatores podem influenciar de forma mais relevante a experiência na plataforma.
    </div>
    """, unsafe_allow_html=True)

if show_device:
    st.subheader("Dispositivo Principal por Tipo de Usuário")

    metric_dev = st.selectbox(
        "Métrica:",
        options=["Contagem de Usuários", "Horas de Escuta Médias"],
        key="sel_device",
    )

    col_dev = "count" if metric_dev == "Contagem de Usuários" else "avg_hours"
    label_dev = "Usuários" if metric_dev == "Contagem de Usuários" else "Horas/Semana"

    device_map = {
        "Mobile": "Celular",
        "Desktop": "Computador",
        "Tablet": "Tablet",
        "Smart Speaker": "Caixa de Som",
        "Car System": "Sistema Automotivo",
    }

    df_dev_pt = df_device.copy()
    df_dev_pt["Tipo de Usuario"] = df_dev_pt["user_type"].map(
        {"Heavy": "Intenso", "Casual": "Casual"}
    ).fillna(df_dev_pt["user_type"])
    df_dev_pt["Dispositivo"] = df_dev_pt["primary_device"].map(device_map).fillna(
        df_dev_pt["primary_device"]
    )

    fig7 = px.bar(
        df_dev_pt,
        x="Dispositivo",
        y=col_dev,
        color="Tipo de Usuario",
        barmode="stack",
        color_discrete_map={"Intenso": GREEN, "Casual": "#3a4055"},
        text=df_dev_pt[col_dev].apply(lambda x: f"{x:.0f}"),
        labels={col_dev: label_dev},
    )

    fig7.update_traces(textposition="inside", **TEXT_STYLE)
    fig7.update_layout(
        **LAYOUT,
        title=dict(text=f"{label_dev} por dispositivo e tipo de usuário", font=TITLE_FONT),
    )
    fig7.update_yaxes(title=label_dev)
    fig7.update_xaxes(title="Dispositivo Principal")

    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("""
    <div class="section-desc">
    <strong>Insight:</strong> A distribuição de usuários entre dispositivos apresentou comportamento bastante equilibrado,
    sem predominância significativa de usuários Intensos ou Casuais em uma plataforma específica.
    As horas médias de escuta também permaneceram estáveis entre os dispositivos, sugerindo
    que o padrão de consumo da plataforma é relativamente consistente independentemente do meio de acesso utilizado.
    </div>
    """, unsafe_allow_html=True)

   
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
<h2 class="final-main-title">
Conclusão Final da Análise
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div class="final-conclusion">

<div class="final-conclusion-text">
<div class="future-title">
Conclusão geral
</div>

<p>
A análise evidenciou padrões relativamente homogêneos de engajamento,
satisfação e consumo entre diferentes perfis de usuários, dispositivos
e grupos de anúncios.
</p>

<p>
Os resultados sugerem que a experiência na plataforma é influenciada por
múltiplos fatores combinados, e não por variáveis isoladas como anúncios,
dispositivo principal ou quantidade de skips.
</p>

<p>
A distribuição equilibrada das funcionalidades desejadas e mais utilizadas
reforça a importância da personalização e da diversidade de recursos como
estratégia de retenção e monetização.
</p>

<hr class="conclusion-divider">

<div class="future-title">
Possíveis Evoluções Analíticas
</div>

<ul class="future-list">
    <li>Análise temporal de comportamento e retenção de usuários;</li>
    <li>Segmentação avançada por perfil musical e frequência de uso;</li>
    <li>Identificação de padrões de churn e recorrência de sessões;</li>
    <li>Correlação entre playlists, gêneros musicais e satisfação;</li>
    <li>Modelos preditivos para conversão premium e engajamento.</li>
</ul>

</div>
</div>
""", unsafe_allow_html=True)