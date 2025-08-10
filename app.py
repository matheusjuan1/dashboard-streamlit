import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(
    page_title="Dashboard de  Salários na Área de Dados",
    page_icon="📊",
    layout="wide"
)

# Carregamento da base de dados
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Barra lateral
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
years_availables = sorted(df['ano'].unique())
selected_years = st.sidebar.multiselect("Ano", years_availables, default=years_availables)

# Filtro de Senioridade
seniority_availables = sorted(df['senioridade'].unique())
selected_seniority = st.sidebar.multiselect("Senioridade", seniority_availables, default=seniority_availables)

# Filtro por Tipo de Contrato
contract_availables = sorted(df['contrato'].unique())
selected_contract = st.sidebar.multiselect("Tipo de Contrato", contract_availables, default=contract_availables)

# Filtro por Tamanho da Empresa
size_availables = sorted(df['tamanho_empresa'].unique())
selected_size = st.sidebar.multiselect("Tamanho da Empresa", size_availables, default=size_availables)

df_filtered = df[
    (df['ano'].isin(selected_years)) &
    (df['senioridade'].isin(selected_seniority)) &
    (df['contrato'].isin(selected_contract)) &
    (df['tamanho_empresa'].isin(selected_size))
]

# Conteúdo Principal
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# Métricas Principais (KPIs)
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtered.empty:
    mean_salary = df_filtered['usd'].mean()
    max_salary = df_filtered['usd'].max()
    registry_count = df_filtered.shape[0]
    most_position_frequency = df_filtered['cargo'].mode()[0]
else:
    mean_salary, max_salary, registry_count, most_position_frequency = 0, 0, 0, "" 
    
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${mean_salary:,.0f}")
col2.metric("Salário máximo", f"${max_salary:,.0f}")
col3.metric("Total de registros", f"{registry_count:,}")
col4.metric("Cargo mais frequente", most_position_frequency)

st.markdown("---")

# Gráficos com Plotly
st.subheader("Gráficos")

col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    if not df_filtered.empty:
        top_positions = df_filtered.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        graph_positions = px.bar(
            top_positions,
            x='usd',
            y='cargo',
            orientation='h',
            title='Top 10 cargos por salário médio',
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        graph_positions.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(graph_positions, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")
        
with col_graph2:
    if not df_filtered.empty:
        hist_graph = px.histogram(
            df_filtered,
            x='usd',
            nbins=30,
            title='Distribuição de salários anuais',
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        hist_graph.update_layout(title_x=0.1)
        st.plotly_chart(hist_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no histograma de salários.")
        
col_graph3, col_graph4 = st.columns(2)

with col_graph3:
    if not df_filtered.empty:
        remote_count = df_filtered['remoto'].value_counts().reset_index()
        remote_count.columns = ['tipo_trabalho', 'quantidade']
        remote_graph = px.pie(
            remote_count,
            names='tipo_trabalho',
            values='quantidade',
            title="Proporção dos tipos de trabalho",
            hole=0.5
        )
        remote_graph.update_traces(textinfo='percent+label')
        remote_graph.update_layout(title_x=0.1)
        st.plotly_chart(remote_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")
        
with col_graph4:
    if not df_filtered.empty:
        df_ds = df_filtered[df_filtered['cargo'] == 'Data Scientist']
        country_mean_salary = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        country_graph = px.choropleth(
        country_mean_salary,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'}
            )
        country_graph.update_layout(title_x=0.1)
        st.plotly_chart(country_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")
        

# Tabela de Dados Detalhados
st.subheader("Dados Detalhados")
st.dataframe(df_filtered)