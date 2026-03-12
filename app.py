import streamlit as st
import pandas as pd
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Qatar 2022 Trends Hub", layout="wide")

st.title("🏆 Analizador de Tendencias: Qatar 2022")
st.markdown("""
Esta herramienta genera enlaces precisos a Google Trends para cada partido, 
utilizando identificadores de entidad para evitar errores de búsqueda.
""")

# --- Función para Cargar Datos ---
@st.cache_data
def load_data():
    try:
        # Intenta cargar el archivo CSV
        return pd.read_csv('partidos_qatar_2022.csv')
    except FileNotFoundError:
        return None

# --- Función para Generar la URL de Google Trends ---
def generate_google_trends_url(row, geo):
    # Google Trends usa el espacio como separador de rango de fechas
    date_range = f"{row['fecha']} {row['fecha']}"
    
    # Comparamos ambos equipos (local vs visitante)
    query = f"{row['id_local']},{row['id_visitante']}"
    
    # Parámetros de la URL
    params = {
        "date": date_range,
        "geo": geo,
        "q": query,
        "hl": "es-419"
    }
    
    # urllib.parse.urlencode se encarga de convertir "/" en "%2F" y "," en "%2C"
    # Esto es VITAL para que Google Trends no tire error.
    base_url = "https://trends.google.com/trends/explore"
    encoded_params = urllib.parse.urlencode(params)
    
    return f"{base_url}?{encoded_params}"

# --- Cuerpo Principal de la App ---
df = load_data()

if df is not None:
    # --- Sidebar: Filtros ---
    st.sidebar.header("Configuración de Análisis")
    
    pais_analisis = st.sidebar.selectbox(
        "País de origen de las búsquedas (GEO)", 
        ["AR", "MX", "ES", "QA", "US", "BR", "FR", "GB"], 
        index=0
    )
    
    fases_disponibles = df['fase'].unique().tolist()
    fase_filtro = st.sidebar.multiselect(
        "Filtrar por Fase del Mundial", 
        fases_disponibles, 
        default=fases_disponibles
    )
    
    # Aplicar filtros al DataFrame
    mask = df['fase'].isin(fase_filtro)
    df_filtered = df[mask].copy()

    # Generar la Columna de URLs usando nuestra función segura
    df_filtered['URL Google Trends'] = df_filtered.apply(
        lambda x: generate_google_trends_url(x, pais_analisis), axis=1
    )

    # --- Mostrar Tabla ---
    st.subheader(f"Partidos Seleccionados - Analizando desde: {pais_analisis}")
    
    st.dataframe(
        df_filtered,
        column_config={
            "URL Google Trends": st.column_config.LinkColumn(
                "Enlace de Análisis", 
                display_text="Ver Tendencias 📈"
            ),
            "fecha": "Fecha",
            "fase": "Etapa",
            "local": "Local",
            "visitante": "Visitante",
            "id_local": None,     # Ocultamos estas columnas técnicas
            "id_visitante": None
        },
        hide_index=True,
        use_container_width=True
    )

    # --- Footer Informativo ---
    st.markdown("---")
    with st.expander("📝 Instrucciones para completar tu reporte (Columnas 5 y 6)"):
        st.write("""
        Para extraer **Búsquedas Relacionadas** y **Temas Relacionados**:
        1. Haz clic en el botón **'Ver Tendencias 📈'** del partido que te interese.
        2. Al abrirse la página de Google Trends, baja hasta la sección final.
        3. Encontrarás los paneles de 'Temas relacionados' y 'Consultas relacionadas'.
        4. Puedes ver los datos directamente o descargarlos en CSV usando el botón ⬇️ en cada panel de Google.
        """)
else:
    st.error("⚠️ No se encontró el archivo **'partidos_qatar_2022.csv'**.")
    st.info("Asegúrate de haber subido el CSV con los 64 partidos a tu repositorio de GitHub.")
