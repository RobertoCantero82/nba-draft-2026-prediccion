import streamlit as st

# ========================
# CONFIGURACIÓN DE LA APP
# ========================

# título y configuración de la página
st.set_page_config(
    page_title="NBA Draft 2026 Predictor",
    page_icon="🏀",
    layout="wide"
)

# ========================
# TÍTULO Y DESCRIPCIÓN
# ========================

st.title("🏀 NBA Draft 2026 Predictor")
st.markdown("Introduce las estadísticas de un jugador y el modelo predecirá su posición en el Draft.")

# línea divisoria
st.divider()

# ========================
# FORMULARIO DE ENTRADA
# ========================

# dividimos la pantalla en dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Estadísticas de cancha")
    # cada número_input es un campo editable
    pts  = st.number_input("PPG (puntos por partido)", min_value=0.0, max_value=40.0, value=12.0, step=0.1)
    reb  = st.number_input("RPG (rebotes por partido)", min_value=0.0, max_value=20.0, value=6.0, step=0.1)
    ast  = st.number_input("APG (asistencias por partido)", min_value=0.0, max_value=15.0, value=2.0, step=0.1)
    bpm  = st.number_input("BPM (impacto en cancha)", min_value=-20.0, max_value=20.0, value=5.0, step=0.1)

with col2:
    st.subheader("Datos físicos")
    # slider para valores con rango
    altura    = st.slider("Altura (cm)", min_value=170, max_value=230, value=200)
    peso      = st.slider("Peso (kg)", min_value=60, max_value=140, value=90)
    enverg    = st.slider("Envergadura (cm)", min_value=170, max_value=240, value=205)
    posicion  = st.selectbox("Posición", ["Base", "Escolta", "Alero", "Ala-Pívot", "Pívot"])

st.divider()

# ========================
# BOTÓN DE PREDICCIÓN
# ========================

# el botón devuelve True cuando se pulsa
if st.button("▶ PREDECIR", type="primary", use_container_width=True):

    # de momento mostramos los datos introducidos
    # aquí irá el modelo cuando lo tengamos entrenado
    st.success("✅ Predicción completada")

    col3, col4, col5 = st.columns(3)

    with col3:
        st.metric("Ronda predicha", "Primera Ronda")
    with col4:
        st.metric("Rango de pick", "1 – 10")
    with col5:
        st.metric("Arquetipo", "Pívot Moderno")