import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------
# Configuração da página
# -------------------------------------------------
st.set_page_config(
    page_title="Do Dado à Decisão",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Do Dado à Decisão")
st.subheader("Criando Relatórios Claros e Impactantes com Dados")

# -------------------------------------------------
# Função para carregar dados
# -------------------------------------------------
@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "data.csv")

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        source = "Arquivo local (data.csv)"
    else:
        df = None
        source = None

    return df, source


df, source = load_data()

# -------------------------------------------------
# Upload opcional (fallback)
# -------------------------------------------------
if df is None:
    st.warning("⚠️ Arquivo data.csv não encontrado na raiz do projeto.")
    uploaded_file = st.file_uploader(
        "Envie o arquivo data.csv para iniciar a análise",
        type="csv"
    )

    if uploaded_file is None:
        st.stop()
    else:
        df = pd.read_csv(uploaded_file)
        source = "Arquivo enviado pelo usuário"

st.success(f"Dados carregados com sucesso — fonte: **{source}**")

# -------------------------------------------------
# Visão geral
# -------------------------------------------------
st.header("📋 Visão Geral dos Dados")

col1, col2, col3 = st.columns(3)
col1.metric("Registros", df.shape[0])
col2.metric("Variáveis", df.shape[1])
col3.metric("Valores ausentes", int(df.isna().sum().sum()))

st.dataframe(df.head())

# -------------------------------------------------
# Sidebar – seleção de colunas
# -------------------------------------------------
st.sidebar.header("🎛️ Configuração da Análise")

col_data = st.sidebar.selectbox(
    "Selecione a coluna de data",
    df.columns
)

col_regiao = st.sidebar.selectbox(
    "Selecione a coluna de região",
    df.columns
)

col_poluente = st.sidebar.selectbox(
    "Selecione a coluna de poluição",
    df.columns
)

# Conversão de data (segura)
df[col_data] = pd.to_datetime(df[col_data], errors="coerce")

# -------------------------------------------------
# Filtro por região
# -------------------------------------------------
regioes = st.sidebar.multiselect(
    "Filtrar regiões",
    options=df[col_regiao].dropna().unique(),
    default=df[col_regiao].dropna().unique()
)

df_filtrado = df[df[col_regiao].isin(regioes)].copy()

# -------------------------------------------------
# Análise temporal (CORRIGIDA)
# -------------------------------------------------
st.header("📈 Tendência Temporal da Poluição")

# Coluna auxiliar de período (evita conflitos)
df_filtrado["_periodo"] = (
    df_filtrado[col_data]
    .dt.to_period("M")
    .dt.to_timestamp()
)

df_time = (
    df_filtrado
    .dropna(subset=["_periodo", col_poluente])
    .groupby("_periodo", as_index=False)[col_poluente]
    .mean()
)

fig1, ax1 = plt.subplots()
sns.lineplot(data=df_time, x="_periodo", y=col_poluente, ax=ax1)
ax1.set_title("Evolução média da poluição ao longo do tempo")
ax1.set_xlabel("Data")
ax1.set_ylabel("Poluição média")

st.pyplot(fig1)

# -------------------------------------------------
# Comparação entre regiões
# -------------------------------------------------
st.header("🏙️ Poluição Média por Região")

df_regiao = (
    df_filtrado
    .groupby(col_regiao)[col_poluente]
    .mean()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots()
df_regiao.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Poluição média")
ax2.set_xlabel("Região")
ax2.set_title("Comparação entre regiões")

st.pyplot(fig2)

# -------------------------------------------------
# Insights automáticos
# -------------------------------------------------
st.header("🧠 Insights para Relatórios")

if not df_regiao.empty:
    regiao_critica = df_regiao.idxmax()
    valor_critico = df_regiao.max()

    st.markdown(f"""
### Principais conclusões:

- Observa-se **variação temporal significativa** nos níveis de poluição analisados.
- A região com **maior concentração média** de poluentes é **{regiao_critica}**.
- O valor médio mais elevado registrado foi **{valor_critico:.2f}**.

Esses resultados reforçam a importância de **ações direcionadas** e **monitoramento contínuo**.
""")
else:
    st.warning("Não foi possível gerar insights com os filtros selecionados.")

# -------------------------------------------------
# Escrita do relatório (atividade pedagógica)
# -------------------------------------------------
st.header("✍️ Escrita do Relatório")

st.markdown("""
Use os gráficos e insights acima para escrever um relatório curto,
em **linguagem clara**, voltado a **gestores públicos não técnicos**.
""")

st.text_area(
    "Relatório (2 parágrafos):",
    height=180,
    placeholder="Exemplo: A análise dos dados indica que..."
)

# -------------------------------------------------
# Rodapé
# -------------------------------------------------
st.markdown("---")
st.caption(
    "Aula prática – Do Dado à Decisão | Visualização, Análise e Comunicação de Dados"
)
