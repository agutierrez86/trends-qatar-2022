import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Qatar 2022 Trends Hub", layout="wide")

st.title("🏆 Analizador de Tendencias: Qatar 2022")
st.markdown("Generador de enlaces masivos para análisis de datos en Google Trends.")

# --- Función para Cargar Datos ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv('partidos_qatar_2022.csv')
    except FileNotFoundError:
        return None

# --- Función para Generar la URL con formato compatible ---
def generate_google_trends_url(row, geo):
    # Google Trends requiere %20 para el espacio en la fecha
    fecha_formateada = f"{row['fecha']}%20{row['fecha']}"
    # Los IDs de entidad deben ir con sus barras y separados por coma simple
    query = f"{row['id_local']},{row['id_visitante']}"
    
    # Construcción manual para evitar que librerías externas alteren los símbolos
    base_url = "https://trends.google.com/trends/explore"
    url = f"{base_url}?date={fecha_formateada}&geo={geo}&q={query}&hl=es-419"
    return url

# --- Cuerpo de la App ---
df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.header("Configuración")
    pais_analisis = st.sidebar.selectbox("País (GEO)", ["AR", "MX", "ES", "QA", "US", "BR"], index=0)
    
    fases = df['fase'].unique().tolist()
    fase_filtro = st.sidebar.multiselect("Filtrar Fase", fases, default=fases)
    
    # Filtrado y Generación de URL
    df_filtered = df[df['fase'].isin(fase_filtro)].copy()
    df_filtered['URL Google Trends'] = df_filtered.apply(lambda x: generate_google_trends_url(x, pais_analisis), axis=1)

    # Mostrar Tabla
    st.subheader(f"Listado de Partidos - Analizando desde {pais_analisis}")
    st.dataframe(
        df_filtered,
        column_config={
            "URL Google Trends": st.column_config.LinkColumn("Analizar", display_text="Ver Tendencias 📈"),
            "id_local": None,
            "id_visitante": None
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.info("Nota: Si el enlace falla, asegúrate de estar logueado en tu cuenta de Google en el navegador.")

else:
    st.error("No se encontró 'partidos_qatar_2022.csv'.")
