import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="World Cup Trends Explorer", layout="wide")

st.title("🏆 World Cup Google Trends Explorer")
st.markdown("Analiza las tendencias de búsqueda de los últimos 3 Mundiales de la FIFA.")

# --- Funciones Core ---
@st.cache_data
def load_data(file_name):
    try:
        return pd.read_csv(file_name)
    except:
        return None

def generate_trends_url(row, geo):
    query = f"{row['local']},{row['visitante']}"
    date_param = f"{row['fecha']} {row['fecha']}"
    params = {"date": date_param, "geo": geo, "q": query, "hl": "es-419"}
    return f"https://trends.google.com/trends/explore?{urllib.parse.urlencode(params)}"

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='TrendsData')
    return output.getvalue()

# --- Configuración en el Sidebar ---
st.sidebar.header("Global Settings")
pais = st.sidebar.selectbox("País de Análisis (GEO)", ["AR", "MX", "ES", "QA", "US", "BR", "RU"], index=0)

# Definición de los mundiales
mundiales = {
    "🇶🇦 Qatar 2022": "partidos_qatar_2022.csv",
    "🇷🇺 Rusia 2018": "partidos_rusia_2018.csv",
    "🇧🇷 Brasil 2014": "partidos_brasil_2014.csv"
}

# Crear Pestañas dinámicamente
tabs = st.tabs(list(mundiales.keys()))

for i, (nombre, archivo) in enumerate(mundiales.items()):
    with tabs[i]:
        df = load_data(archivo)
        if df is not None:
            st.subheader(f"Partidos de {nombre}")
            
            # Generar URLs
            df['URL Google Trends'] = df.apply(lambda x: generate_trends_url(x, pais), axis=1)
            
            # Botón de descarga
            st.download_button(
                label=f"📥 Descargar {nombre} (Excel)",
                data=to_excel(df),
                file_name=f"trends_{archivo.split('.')[0]}.xlsx",
                key=f"btn_{i}"
            )
            
            # Mostrar Tabla
            st.dataframe(
                df[['fecha', 'fase', 'local', 'visitante', 'URL Google Trends']], 
                column_config={
                    "URL Google Trends": st.column_config.LinkColumn("Link", display_text="Ver 📈")
                },
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.warning(f"Archivo '{archivo}' no encontrado en el repositorio.")

st.sidebar.markdown("---")
st.sidebar.info("💡 Consejo: Selecciona el país (GEO) para ver cómo cambiaron las tendencias según la región.")
