import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "iot_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def get_db_connection():
    return create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def processar_dados(df):
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]
    df = df.rename(columns={
        'room_id/id': 'room_id',
        'noted_date': 'noted_date',
        'temp': 'temperature',
        'out/in': 'location_type'
    })
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
    return df

def create_views(engine):
    views_sql = [
        """
        CREATE OR REPLACE VIEW avg_temp_por_local AS
        SELECT room_id, AVG(temperature) as avg_temp
        FROM temperature_logs
        GROUP BY room_id;
        """,
        """
        CREATE OR REPLACE VIEW leituras_por_hora AS
        SELECT EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) as hora, COUNT(*) as contagem
        FROM temperature_logs
        GROUP BY EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI'))
        ORDER BY hora;
        """,
        """
        CREATE OR REPLACE VIEW temp_max_min_por_dia AS
        SELECT TO_DATE(SUBSTRING(noted_date FROM 7 FOR 4) || '-' || SUBSTRING(noted_date FROM 4 FOR 2) || '-' || SUBSTRING(noted_date FROM 1 FOR 2), 'YYYY-MM-DD') as data, 
               MAX(temperature) as temp_max, 
               MIN(temperature) as temp_min
        FROM temperature_logs
        GROUP BY TO_DATE(SUBSTRING(noted_date FROM 7 FOR 4) || '-' || SUBSTRING(noted_date FROM 4 FOR 2) || '-' || SUBSTRING(noted_date FROM 1 FOR 2), 'YYYY-MM-DD')
        ORDER BY data;
        """,
        """
        CREATE OR REPLACE VIEW temp_por_localizacao AS
        SELECT location_type, 
               AVG(temperature) as avg_temp,
               MAX(temperature) as temp_max,
               MIN(temperature) as temp_min,
               COUNT(*) as total_leituras
        FROM temperature_logs
        GROUP BY location_type;
        """,
        """
        CREATE OR REPLACE VIEW temp_media_por_dia AS
        SELECT TO_DATE(SUBSTRING(noted_date FROM 7 FOR 4) || '-' || SUBSTRING(noted_date FROM 4 FOR 2) || '-' || SUBSTRING(noted_date FROM 1 FOR 2), 'YYYY-MM-DD') as data, 
               AVG(temperature) as temp_media
        FROM temperature_logs
        GROUP BY TO_DATE(SUBSTRING(noted_date FROM 7 FOR 4) || '-' || SUBSTRING(noted_date FROM 4 FOR 2) || '-' || SUBSTRING(noted_date FROM 1 FOR 2), 'YYYY-MM-DD')
        ORDER BY data;
        """,
        """
        CREATE OR REPLACE VIEW contagem_por_localizacao AS
        SELECT room_id, location_type, COUNT(*) as total
        FROM temperature_logs
        GROUP BY room_id, location_type;
        """
    ]
    with engine.connect() as conn:
        for view_sql in views_sql:
            conn.execute(text(view_sql))
        conn.commit()

def load_data(view_name):
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, get_db_connection())

st.set_page_config(page_title="Dashboard IoT - Temperaturas", layout="wide")

st.title("Dashboard de Temperaturas - IoT Devices")
st.markdown("---")

tab1, tab2 = st.tabs([" Upload de Dados", " Visualizações"])

with tab1:
    st.header("Upload de Arquivo CSV")
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Estrutura do Dataset:")
        st.write(df.head())
        st.write(f"Linhas: {len(df)}, Colunas: {len(df.columns)}")
        
        if st.button("Enviar para o Banco de Dados"):
            try:
                df_processado = processar_dados(df)
                engine = get_db_connection()
                with engine.connect() as conn:
                    conn.execute(text("DROP TABLE IF EXISTS temperature_logs CASCADE"))
                    conn.execute(text("DROP VIEW IF EXISTS avg_temp_por_local CASCADE"))
                    conn.execute(text("DROP VIEW IF EXISTS leituras_por_hora CASCADE"))
                    conn.execute(text("DROP VIEW IF EXISTS temp_max_min_por_dia CASCADE"))
                    conn.commit()
                df_processado.to_sql('temperature_logs', engine, if_exists='replace', index=False)
                create_views(engine)
                st.success(f"Dados enviados para o banco de dados! {len(df_processado)} linhas inseridas.")
            except Exception as e:
                st.error(f"Erro ao conectar ao banco: {e}")

with tab2:
    st.header("Visualizações dos Dados")
    
    try:
        engine = get_db_connection()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Média de Temperatura por Local")
            df_avg = load_data('avg_temp_por_local')
            if not df_avg.empty:
                fig1 = px.bar(df_avg, x='room_id', y='avg_temp', 
                           color='room_id', title="Temperatura Média por Sala")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("Leituras por Hora do Dia")
            df_hora = load_data('leituras_por_hora')
            if not df_hora.empty:
                fig2 = px.line(df_hora, x='hora', y='contagem', 
                             markers=True, title="Contagem de Leituras por Hora")
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("Temperaturas Máximas e Mínimas por Dia")
        df_temp = load_data('temp_max_min_por_dia')
        if not df_temp.empty:
            df_melted = df_temp.melt(id_vars=['data'], 
                                  value_vars=['temp_max', 'temp_min'],
                                  var_name='Tipo', value_name='Temperatura')
            fig3 = px.line(df_melted, x='data', y='Temperatura', color='Tipo',
                         title="Temperatura Máxima e Mínima por Dia")
            st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("---")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Estatísticas por Localização (In/Out)")
            df_loc = load_data('temp_por_localizacao')
            if not df_loc.empty:
                fig4 = px.bar(df_loc, x='location_type', y='avg_temp',
                            color='location_type', title="Temperatura Média: Inside vs Outside")
                st.plotly_chart(fig4, use_container_width=True)
        
        with col4:
            st.subheader("Contagem por Sala e Localização")
            df_cont = load_data('contagem_por_localizacao')
            if not df_cont.empty:
                fig5 = px.bar(df_cont, x='room_id', y='total',
                            color='location_type', barmode='group', title="Leituras por Sala")
                st.plotly_chart(fig5, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("Dados Bruto - Primeiras 100 linhas")
        df_raw = pd.read_sql("SELECT * FROM temperature_logs LIMIT 100", engine)
        st.dataframe(df_raw, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar visualizações: {e}")
        st.info("Faça o upload de um arquivo CSV na aba 'Upload de Dados' primeiro.")