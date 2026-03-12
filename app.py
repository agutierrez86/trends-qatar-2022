import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Sara vigila el Mundial 🏆", layout="wide", page_icon="🏆")

# Título Principal
st.title("🏆 Sara vigila el Mundial")
st.markdown("### Monitor de Tendencias: Previa, Durante y Después")

# --- Funciones Core ---
@st.cache_data
def load_data(file_name):
    try:
        return pd.read_csv(file_name)
    except:
        return None

def generate_trends_url(row, geo, modo):
    query = f"{row['local']},{row['visitante']}"
    fecha_dt = datetime.strptime(row['fecha'], '%Y-%m-%d')
    
    if modo == "Previa":
        # 2 días antes del partido
        f_inicio = (fecha_dt - timedelta(days=2)).strftime('%Y-%m-%d')
        f_fin = (fecha_dt - timedelta(days=1)).strftime('%Y-%m-%d')
    elif modo == "Durante":
        # El mismo día del partido
        f_inicio = row['fecha']
        f_fin = row['fecha']
    elif modo == "Despues":
        # 2 días después del partido
        f_inicio = (fecha_dt + timedelta(days=1)).strftime('%Y-%m-%d')
        f_fin = (fecha_dt + timedelta(days=2)).strftime('%Y-%m-%d')
    
    date_param = f"{f_inicio} {f_fin}"
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

mundiales = {
    "🇶🇦 Qatar 2022": "partidos_qatar_2022.csv",
    "🇷🇺 Rusia 2018": "partidos_rusia_2018.csv",
    "🇧🇷 Brasil 2014": "partidos_brasil_2014.csv"
}

tabs = st.tabs(list(mundiales.keys()))

for i, (nombre, archivo) in enumerate(mundiales.items()):
    with tabs[i]:
        df = load_data(archivo)
        if df is not None:
            st.subheader(f"Partidos de {nombre}")
            
            # Generar las 3 columnas de URLs
            df['Previa (2 días antes)'] = df.apply(lambda x: generate_trends_url(x, pais, "Previa"), axis=1)
            df['Durante (Día del partido)'] = df.apply(lambda x: generate_trends_url(x, pais, "Durante"), axis=1)
            df['Después (2 días después)'] = df.apply(lambda x: generate_trends_url(x, pais, "Despues"), axis=1)
            
            # Botón de descarga
            st.download_button(
                label=f"📥 Descargar {nombre} (Excel)",
                data=to_excel(df),
                file_name=f"vigilancia_{archivo.split('.')[0]}.xlsx",
                key=f"btn_{i}"
            )
            
            # Mostrar Tabla con las nuevas columnas
            st.dataframe(
                df[['fecha', 'fase', 'local', 'visitante', 'Previa (2 días antes)', 'Durante (Día del partido)', 'Después (2 días después)']], 
                column_config={
                    "Previa (2 días antes)": st.column_config.LinkColumn("Previa", display_text="🔍"),
                    "Durante (Día del partido)": st.column_config.LinkColumn("Durante", display_text="⚽"),
                    "Después (2 días después)": st.column_config.LinkColumn("Después", display_text="📉")
                },
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.warning(f"Archivo '{archivo}' no encontrado.")

# --- Firma en el Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>Desarrollado por <strong>Agustín Gutierrez</strong></p>
        <a href="https://www.linkedin.com/in/agutierrez86/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30" height="30" style="vertical-align: middle; margin-right: 10px;">
            Conéctame en LinkedIn
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

