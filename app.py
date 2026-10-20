import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Analítico Interativo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS ---
@st.cache_data
def load_data():
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    regions = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    categories = ["Eletrônicos", "Móveis", "Vestuário"]
    
    np.random.seed(42)
    data = []
    for d in dates:
        for r in regions:
            for c in categories:
                data.append({
                    "Data": d,
                    "Região": r,
                    "Categoria": c,
                    "Vendas": np.random.randint(100, 1500),
                    "Lucro": np.random.randint(20, 400)
                })
    return pd.DataFrame(data)

df = load_data()

# --- TÍTULO E INTRODUÇÃO ---
st.title("📊 Painel de Desempenho Comercial")
st.markdown("*Aplicações do Mantra de Shneiderman e Visões Coordenadas (Brushing & Linking)*")

# --- BARRA LATERAL: INTERAÇÃO E FILTROS (Zoom & Filter) ---
st.sidebar.header("🔍 Filtros de Interação")

regioes_selecionadas = st.sidebar.multiselect(
    "Selecione as Regiões:",
    options=df["Região"].unique(),
    default=df["Região"].unique()
)

categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as Categorias:",
    options=df["Categoria"].unique(),
    default=df["Categoria"].unique()
)

# Aplicação do filtro global (Linking)
df_filtered = df[
    (df["Região"].isin(regioes_selecionadas)) & 
    (df["Categoria"].isin(categorias_selecionadas))
]

# --- PAINEL PRINCIPAL: VISÕES COORDENADAS ---
col1, col2 = st.columns(2)

# 1. VISÃO GERAL TEMPORAL (Overview)
with col1:
    st.subheader("1. Evolução Temporal das Vendas")
    df_temp = df_filtered.groupby("Data")["Vendas"].sum().reset_index()
    fig_temp = px.line(
        df_temp, 
        x="Data", 
        y="Vendas",
        color_discrete_sequence=["#2b5c8f"],
        template="plotly_white"
    )
    fig_temp.update_traces(hovertemplate="<b>Data:</b> %{x}<br><b>Vendas:</b> R$ %{y:,.2f}")
    fig_temp.update_layout(xaxis_title="", yaxis_title="Vendas (R$)", margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_temp, use_container_width=True)

# 2. DISTRIBUIÇÃO CATEGÓRICA (Categorical Distribution)
with col2:
    st.subheader("2. Vendas por Categoria")
    df_cat = df_filtered.groupby("Categoria")["Vendas"].sum().reset_index().sort_values(by="Vendas", ascending=True)
    fig_cat = px.bar(
        df_cat, 
        x="Vendas", 
        y="Categoria", 
        orientation="h",
        color="Vendas",
        color_continuous_scale="Viridis",
        template="plotly_white"
    )
    fig_cat.update_traces(hovertemplate="<b>Categoria:</b> %{y}<br><b>Total:</b> R$ %{x:,.2f}")
    fig_cat.update_layout(xaxis_title="Vendas (R$)", yaxis_title="", showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_cat, use_container_width=True)

# 3. DETALHES SOB DEMANDA (Details-on-Demand)
st.markdown("---")
st.subheader("3. Detalhes Sob Demanda")

with st.expander("📋 Visualizar Tabela de Dados Detalhada", expanded=True):
    st.dataframe(
        df_filtered.style.format({"Vendas": "R$ {:,.2f}", "Lucro": "R$ {:,.2f}"}),
        use_container_width=True,
        height=250
    )
