import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Trends Qatar 2022", layout="wide")

st.title("🏆 Google Trends: Qatar 2022")

@st.cache_data
def load_data():
    try:
        # Cargamos el CSV que ya tienes en GitHub
        return pd.read_csv('partidos_qatar_2022.csv')
    except:
        return None

def generate_trends_url(row, geo):
    # En lugar de usar los IDs que dan error 404, usamos los nombres de los equipos
    # Esto es mucho más estable para generar links externos
    query = f"{row['local']},{row['visitante']}"
    
    # Rango de fecha: día del partido y el siguiente para capturar todo el volumen
    # Google Trends acepta mejor rangos de al menos 2 días para términos de texto
    fecha_inicio = row['fecha']
    # Creamos un rango de un día (ej: 2022-11-20 2022-11-20)
    date_param = f"{fecha_inicio} {fecha_inicio}"
    
    params = {
        "date": date_param,
        "geo": geo,
        "q": query,
        "hl": "es-419"
    }
    
    base_url = "https://trends.google.com/trends/explore"
    # urlencode se encarga de que los espacios y comas sean correctos
    encoded_params = urllib.parse.urlencode(params)
    
    return f"{base_url}?{encoded_params}"

df = load_data()

if df is not None:
    st.sidebar.header("Filtros")
    pais = st.sidebar.selectbox("País (GEO)", ["AR", "MX", "ES", "QA", "US", "BR"], index=0)
    
    # Generar URLs basadas en nombres de equipos
    df['URL'] = df.apply(lambda x: generate_trends_url(x, pais), axis=1)
    
    # Tabla
    st.dataframe(
        df[['fecha', 'fase', 'local', 'visitante', 'URL']],
        column_config={
            "URL": st.column_config.LinkColumn("Enlace Trends", display_text="Ver Tendencias 📈"),
            "fecha": "Fecha",
            "local": "Local",
            "visitante": "Visitante"
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.info("💡 Al usar nombres de equipos en lugar de IDs técnicos, los enlaces son ahora compatibles con todos los navegadores.")
else:
    st.error("No se encontró 'partidos_qatar_2022.csv'.")
