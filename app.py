import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

# Configuración de la página con el logo de la copa 🏆
st.set_page_config(page_title="Sara vigila el Mundial 🏆", layout="wide", page_icon="🏆")

# Título Principal
st.title("🏆 Sara vigila el Mundial")
st.markdown("### Análisis histórico de tendencias: Brasil 2014, Rusia 2018 y Qatar 2022")

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
st.sidebar.header("Configuración Global")
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
            
            df['URL Google Trends'] = df.apply(lambda x: generate_trends_url(x, pais), axis=1)
            
            st.download_button(
                label=f"📥 Descargar {nombre} (Excel)",
                data=to_excel(df),
                file_name=f"trends_{archivo.split('.')[0]}.xlsx",
                key=f"btn_{i}"
            )
            
            st.dataframe(
                df[['fecha', 'fase', 'local', 'visitante', 'URL Google Trends']], 
                column_config={
                    "URL Google Trends": st.column_config.LinkColumn("Link", display_text="Ver 📈")
                },
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.warning(f"Archivo '{archivo}' no encontrado.")

# --- Firma en el Footer con tu LinkedIn ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>Desarrollado por <strong>Sara</strong></p>
        <a href="https://www.linkedin.com/in/agutierrez86/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30" height="30" style="vertical-align: middle; margin-right: 10px;">
            Conéctame en LinkedIn
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.info("🏆 **Sara vigila cada búsqueda.**")
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado con ❤️ por Sara")
