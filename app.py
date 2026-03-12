import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Qatar 2022 Trends Hub", layout="wide")

st.title("🏆 Analizador de Tendencias: Qatar 2022")

# Cargar Datos
@st.cache_data
def load_data():
    # Asegúrate de tener el archivo CSV en la misma carpeta
    return pd.read_csv('partidos_qatar_2022.csv')

try:
    df = load_data()

    # --- Sidebar: Filtros ---
    st.sidebar.header("Filtros de Búsqueda")
    pais_analisis = st.sidebar.selectbox("País de origen de las búsquedas (GEO)", 
                                        ["AR", "MX", "ES", "QA", "US", "BR"], index=0)
    
    fase_filtro = st.sidebar.multiselect("Filtrar por Fase", df['fase'].unique(), default=df['fase'].unique())
    
    # --- Lógica de Generación de URL ---
   def generate_google_trends_url(row, geo):
    # Usamos %20 explícitamente para el espacio entre fechas
    date_range = f"{row['fecha']}%20{row['fecha']}"
    
    # La coma entre IDs a veces da error si se codifica, 
    # la dejamos simple o usamos %2C
    query = f"{row['id_local']},{row['id_visitante']}"
    
    # Construimos la URL manualmente para asegurar el formato exacto que Google acepta
    url = (
        f"https://trends.google.com/trends/explore"
        f"?date={date_range}"
        f"&geo={geo}"
        f"&q={query}"
        f"&hl=es-419"
    )
    return url

    # Aplicar filtros
    mask = df['fase'].isin(fase_filtro)
    df_filtered = df[mask].copy()

    # Generar la Columna 4
    df_filtered['URL Google Trends'] = df_filtered.apply(lambda x: generate_google_trends_url(x, pais_analisis), axis=1)

    # --- Mostrar Tabla ---
    st.subheader(f"Partidos Seleccionados - Analizando desde: {pais_analisis}")
    
    # Configuración estética de la tabla
    st.dataframe(
        df_filtered,
        column_config={
            "URL Google Trends": st.column_config.LinkColumn("Abrir en Google Trends", display_text="Ver Análisis 📈"),
            "fecha": "Fecha",
            "local": "Equipo Local",
            "visitante": "Equipo Visitante"
        },
        hide_index=True,
        use_container_width=True
    )

    # --- Instrucciones para Columnas 5 y 6 ---
    st.markdown("---")
    with st.expander("ℹ️ Cómo completar las Columnas 5 y 6 (Búsquedas y Temas Relacionados)"):
        st.write("""
        1. Haz clic en **'Ver Análisis 📈'** para abrir la URL generada.
        2. Desliza hasta el final de la página de Google Trends.
        3. Verás los cuadros de **'Temas relacionados'** y **'Consultas relacionadas'**.
        4. Puedes exportar esos datos directamente desde Google Trends a CSV haciendo clic en el icono de flecha hacia abajo (⬇️) en cada cuadro.
        """)

except FileNotFoundError:
    st.error("No se encontró el archivo 'partidos_qatar_2022.csv'. Por favor, créalo con los datos proporcionados.")
