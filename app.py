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
    # Forzamos los parámetros tal cual los espera Google
    # %20 es el espacio, y evitamos cualquier otra codificación
    base = "https://trends.google.com/trends/explore"
    date_part = f"date={row['fecha']}%20{row['fecha']}"
    geo_part = f"geo={geo}"
    q_part = f"q={row['id_local']},{row['id_visitante']}"
    hl_part = "hl=es-419"
    
    # Unimos todo con '&' manualmente
    return f"{base}?{date_part}&{geo_part}&{q_part}&{hl_part}"

df = load_data()

if df is not None:
    st.sidebar.header("Filtros")
    pais = st.sidebar.selectbox("País (GEO)", ["AR", "MX", "ES", "QA", "US", "BR"], index=0)
    
    # Procesar
    df['URL'] = df.apply(lambda x: generate_trends_url(x, pais), axis=1)
    
    # Mostrar tabla con configuración de columna de enlace clásica
    st.dataframe(
        df[['fecha', 'fase', 'local', 'visitante', 'URL']],
        column_config={
            "URL": st.column_config.LinkColumn("Enlace Trends", display_text="Abrir gráfico 📈")
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("""
    ---
    **💡 Si el enlace falla al hacer clic:**
    Google a veces bloquea el 'salto' desde apps externas. Si ves una página de error:
    1. Haz **click derecho** sobre 'Abrir gráfico'.
    2. Selecciona **'Abrir enlace en una ventana de incógnito'**.
    3. Esto suele saltarse las restricciones de cookies de Google.
    """)
else:
    st.error("No se encontró el archivo CSV.")
