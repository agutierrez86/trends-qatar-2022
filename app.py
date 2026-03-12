import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trends Qatar 2022", layout="wide")

st.title("🏆 Google Trends: Qatar 2022")

@st.cache_data
def load_data():
    try:
        return pd.read_csv('partidos_qatar_2022.csv')
    except:
        return None

def generate_trends_url(row, geo):
    # Paso 1: Codificamos manualmente los IDs para que Google no se confunda
    # Reemplazamos "/" por "%2F"
    id1 = row['id_local'].replace("/", "%2F")
    id2 = row['id_visitante'].replace("/", "%2F")
    
    # Paso 2: Construimos la query comparativa separada por coma codificada (%2C)
    q_param = f"{id1}%2C{id2}"
    
    # Paso 3: Rango de fecha con espacio codificado (%20)
    date_param = f"{row['fecha']}%20{row['fecha']}"
    
    base_url = "https://trends.google.com/trends/explore"
    return f"{base_url}?date={date_param}&geo={geo}&q={q_param}&hl=es-419"

df = load_data()

if df is not None:
    st.sidebar.header("Filtros")
    pais = st.sidebar.selectbox("País (GEO)", ["AR", "MX", "ES", "QA", "US", "BR"], index=0)
    
    # Generar URLs con la nueva lógica de codificación
    df['URL'] = df.apply(lambda x: generate_trends_url(x, pais), axis=1)
    
    # Tabla limpia
    st.dataframe(
        df[['fecha', 'fase', 'local', 'visitante', 'URL']],
        column_config={
            "URL": st.column_config.LinkColumn("Enlace Trends", display_text="Ver Comparativa 📈")
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.error("Archivo CSV no detectado.")
