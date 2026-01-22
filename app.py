import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Configurações iniciais
# -----------------------------
st.set_page_config(
    page_title="Qualidade do Ar - Análise e Relatórios",
    layout="wide"
)

st.title("🌫️ Análise da Qualidade do Ar")
st.subheader("Exploração de dados para apoiar decisões públicas")

# -----------------------------
# Carregamento dos dados
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

st.success("Dados carregados com sucesso!")

# -----------------------------
# Visão geral
# -----------------------------
st.header("📊 Visão Geral dos Dados")
st.dataframe(df.head())

st.markdown(f"""
- **Número de registros:** {df.shape[0]}
- **Número de variáveis:** {df.shape[1]}
""")

# -----------------------------
# Sidebar - Filtros
# -----------------------------
st.sidebar.header("🎛️ Filtros")

# Ajuste os nomes conforme seu CSV
col_data = st.sidebar.selectbox("Coluna de data:", df.columns)
df[col_data] = pd.to_datetime(df[col_data])

col_regiao = st.sidebar.selectbox("Coluna de região:", df.columns)
col_poluente = st.sidebar.selectbox("Coluna de poluente:", df.columns)

regioes = st.sidebar.multiselect(
    "Selecione as regiões:",
    df[col_regiao].unique(),
    default=df[col_regiao].unique()
)

df_filtrado = df[df[col_regiao].isin(regioes)]

# -----------------------------
# Análise temporal
# -----------------------------
st.header("📈 Tendência Temporal da Poluição")

df_time = (
    df_filtrado
    .groupby(pd.Grouper(key=col_data, freq="M"))[col_poluente]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots()
sns.lineplot(data=df_time, x=col_data, y=col_poluente, ax=ax)
ax.set_title("Evolução média da poluição ao longo do tempo")
ax.set_xlabel("Data")
ax.set_ylabel("Nível médio de poluição")

st.pyplot(fig)

# -----------------------------
# Comparação entre regiões
# -----------------------------
st.header("🏙️ Comparação entre Regiões")

df_regiao = (
    df_filtrado
    .groupby(col_regiao)[col_poluente]
    .mean()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots()
df_regiao.plot(kind="bar", ax=ax2)
ax2.set_title("Média de poluição por região")
ax2.set_ylabel("Poluição média")

st.pyplot(fig2)

# -----------------------------
# Insights para Relatórios
# -----------------------------
st.header("📝 Insights para Relatórios")

regiao_critica = df_regiao.idxmax()
valor_critico = df_regiao.max()

st.markdown(f"""
**Principais insights gerados automaticamente:**

- A poluição apresenta **variações sazonais claras**, com picos ao longo do tempo analisado.
- A região com **maior nível médio de poluição** é **{regiao_critica}**.
- O valor médio mais elevado registrado foi **{valor_critico:.2f}**.
""")

st.info("Esses insights devem ser traduzidos em linguagem clara para gestores públicos não técnicos.")

# -----------------------------
# Área de reflexão
# -----------------------------
st.header("💡 Reflexão Final")

st.text_area(
    "Escreva um parágrafo de relatório baseado nos dados:",
    height=150,
    placeholder="Exemplo: Os dados indicam que..."
)
