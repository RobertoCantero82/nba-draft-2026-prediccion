import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ========================
# PALETA DE COLORES
# (extraída de presentacion_final_draft.html)
# ========================
COLOR_FONDO      = "#0a1019"   # azul muy oscuro
COLOR_ACENTO     = "#f97316"   # naranja
COLOR_TEXTO      = "#f0f4ff"   # blanco azulado
COLOR_SECUNDARIO = "#2a1215"   # granate oscuro
COLOR_GRIS       = "#999"

# ========================
# CSS PERSONALIZADO
# ========================
st.markdown(f"""
<style>
  /* Fondo general */
  .stApp {{
      background-color: {COLOR_FONDO};
  }}
  /* Encabezados */
  h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
      color: {COLOR_TEXTO} !important;
      font-family: 'Oswald', 'Arial Narrow', sans-serif !important;
      letter-spacing: 1px;
  }}
  /* Texto general */
  p, label, .stMarkdown p, .stMarkdown {{
      color: {COLOR_TEXTO} !important;
  }}
  /* Subheaders con acento naranja */
  .stApp [data-testid="stSubheader"] {{
      color: {COLOR_ACENTO} !important;
      font-weight: 700;
      border-bottom: 2px solid {COLOR_ACENTO};
      padding-bottom: 4px;
  }}
  /* Inputs y sliders */
  .stNumberInput input, .stSelectbox select {{
      background-color: #1a2535 !important;
      color: {COLOR_TEXTO} !important;
      border: 1px solid {COLOR_ACENTO}44 !important;
  }}
  /* Slider acento naranja */
  .stSlider [data-baseweb="slider"] div[role="slider"] {{
      background-color: {COLOR_ACENTO} !important;
  }}
  /* Botón principal */
  .stButton > button[kind="primary"] {{
      background-color: {COLOR_ACENTO} !important;
      color: #fff !important;
      font-weight: 700 !important;
      font-family: 'Oswald', 'Arial Narrow', sans-serif !important;
      letter-spacing: 2px !important;
      border: none !important;
      border-radius: 4px !important;
      font-size: 1rem !important;
  }}
  .stButton > button[kind="primary"]:hover {{
      opacity: 0.85;
  }}
  /* Métricas */
  [data-testid="stMetricLabel"] {{
      color: {COLOR_GRIS} !important;
      font-size: 0.8rem !important;
      text-transform: uppercase;
      letter-spacing: 1px;
  }}
  [data-testid="stMetricValue"] {{
      color: {COLOR_ACENTO} !important;
      font-weight: 700 !important;
      font-family: 'Oswald', 'Arial Narrow', sans-serif !important;
  }}
  /* Dividers */
  hr {{
      border-color: {COLOR_ACENTO}44 !important;
  }}
  /* Success box */
  .stSuccess {{
      background-color: {COLOR_SECUNDARIO} !important;
      color: {COLOR_TEXTO} !important;
      border-left: 4px solid {COLOR_ACENTO} !important;
  }}
  /* Sidebar y general */
  section[data-testid="stSidebar"] {{
      background-color: #111827 !important;
  }}
</style>
""", unsafe_allow_html=True)

# ========================
# TABLA DE JUGADORES COMPARABLES
# ========================
jugadores_comparables = {
    "Kristaps Porzingis": {
        "stats_norm": [7.0, 5.5, 2.0, 6.5, 9.5, 9.0],
        "arquetipo": "Pívot Moderno",
        "descripcion": "Pívot anotador con tiro exterior élite y gran envergadura defensiva.",
        "busqueda_youtube": "Kristaps Porzingis NBA highlights"
    }
}

# ========================
# CONFIGURACIÓN DE LA APP
# ========================
st.set_page_config(
    page_title="NBA Draft 2026 Predictor",
    page_icon="🏀",
    layout="wide"
)

# ========================
# TÍTULO Y DESCRIPCIÓN
# ========================
st.markdown(f"""
<h1 style='text-align:center; color:{COLOR_ACENTO}; font-family:Oswald,Arial Narrow,sans-serif;
    letter-spacing:3px; font-size:2.4rem; margin-bottom:0;'>
    🏀 NBA DRAFT 2026 PREDICTOR 🏀
</h1>
<p style='text-align:center; color:{COLOR_GRIS}; font-size:0.95rem; margin-top:6px;
    letter-spacing:1px;'>
    Introduce las estadísticas de un jugador y el modelo predecirá su posición en el Draft.
</p>
""", unsafe_allow_html=True)

st.divider()

# ========================
# FORMULARIO DE ENTRADA
# ========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Estadísticas de cancha")
    pts  = st.number_input("PPG (puntos por partido)", min_value=0.0, max_value=40.0, value=12.0, step=0.1)
    reb  = st.number_input("RPG (rebotes por partido)", min_value=0.0, max_value=20.0, value=6.0, step=0.1)
    ast  = st.number_input("APG (asistencias por partido)", min_value=0.0, max_value=15.0, value=2.0, step=0.1)
    bpm  = st.number_input("BPM (impacto en cancha)", min_value=-20.0, max_value=20.0, value=5.0, step=0.1)

with col2:
    st.subheader("Datos físicos")
    altura   = st.slider("Altura (cm)", min_value=170, max_value=230, value=200)
    peso     = st.slider("Peso (kg)", min_value=60, max_value=140, value=90)
    enverg   = st.slider("Envergadura (cm)", min_value=170, max_value=240, value=205)
    posicion = st.selectbox("Posición", ["Base", "Escolta", "Alero", "Ala-Pívot", "Pívot"])

st.divider()

# ========================
# RADAR CHART EN TIEMPO REAL
# ========================
st.subheader("📊 Perfil del jugador")

# normalización a escala 0-10
pts_norm    = round((pts / 40.0) * 10, 2)
reb_norm    = round((reb / 20.0) * 10, 2)
ast_norm    = round((ast / 15.0) * 10, 2)
bpm_norm    = round(((bpm + 20) / 40.0) * 10, 2)
altura_norm = round(((altura - 170) / 60.0) * 10, 2)
enverg_norm = round(((enverg - 170) / 70.0) * 10, 2)

categorias      = ["Anotación", "Rebote", "Asistencias", "Impacto (BPM)", "Altura", "Envergadura"]
valores_jugador = [pts_norm, reb_norm, ast_norm, bpm_norm, altura_norm, enverg_norm]
valores_ref     = [5.5, 4.5, 3.5, 5.5, 6.0, 6.0]   # media picks 15-30

# cerrar polígono
cat_c  = categorias + [categorias[0]]
jug_c  = valores_jugador + [valores_jugador[0]]
ref_c  = valores_ref + [valores_ref[0]]

fig = go.Figure()

# referencia
fig.add_trace(go.Scatterpolar(
    r=ref_c, theta=cat_c,
    fill='toself',
    fillcolor='rgba(153,153,153,0.1)',
    line=dict(color=COLOR_GRIS, width=1.5, dash='dash'),
    name='Media picks 15-30'
))

# jugador
fig.add_trace(go.Scatterpolar(
    r=jug_c, theta=cat_c,
    fill='toself',
    fillcolor='rgba(249,115,22,0.2)',
    line=dict(color=COLOR_ACENTO, width=2.5),
    name='Jugador actual'
))

fig.update_layout(
    polar=dict(
        bgcolor='rgba(10,16,25,0)',
        radialaxis=dict(
            visible=True, range=[0, 10],
            tickfont=dict(size=9, color=COLOR_GRIS),
            gridcolor='rgba(249,115,22,0.2)',
            linecolor='rgba(249,115,22,0.3)'
        ),
        angularaxis=dict(
            tickfont=dict(size=11, color=COLOR_TEXTO),
            linecolor='rgba(249,115,22,0.3)'
        )
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    legend=dict(
        orientation='h', yanchor='bottom', y=-0.18,
        xanchor='center', x=0.5,
        font=dict(color=COLOR_TEXTO)
    ),
    margin=dict(t=30, b=70, l=60, r=60),
    height=420
)

col_vacia1, col_grafico, col_vacia2 = st.columns([1, 2, 1])
with col_grafico:
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ========================
# BOTÓN DE PREDICCIÓN
# ========================
if st.button("▶ PREDICCIÓN", type="primary", use_container_width=True):

    st.success("✅ Predicción completada")

    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("Ronda predicha", "Primera Ronda")
    with col4:
        st.metric("Rango de pick", "1 – 10")
    with col5:
        st.metric("Arquetipo", "Pívot Moderno")

    st.divider()

    # ========================
    # JUGADOR COMPARABLE
    # ========================
    vector_jugador = np.array([pts_norm, reb_norm, ast_norm, bpm_norm, altura_norm, enverg_norm])

    distancias = {}
    for nombre, datos in jugadores_comparables.items():
        vector_ref = np.array(datos["stats_norm"])
        distancias[nombre] = np.linalg.norm(vector_jugador - vector_ref)

    nombre_comparable = min(distancias, key=distancias.get)
    datos_comparable  = jugadores_comparables[nombre_comparable]

    st.subheader("🔍 Jugador comparable")

    col_info, col_video = st.columns([1, 2])

    with col_info:
        st.markdown(f"""
        <div style='background:{COLOR_SECUNDARIO}; border-left:3px solid {COLOR_ACENTO};
             padding:20px; border-radius:6px;'>
            <h3 style='color:{COLOR_ACENTO}; font-family:Oswald,sans-serif;
                margin-bottom:8px;'>👤 {nombre_comparable}</h3>
            <p style='color:{COLOR_GRIS}; font-size:0.8rem; text-transform:uppercase;
                letter-spacing:1px; margin-bottom:4px;'>Arquetipo</p>
            <p style='color:{COLOR_TEXTO}; font-weight:700; margin-bottom:12px;'>
                {datos_comparable['arquetipo']}</p>
            <p style='color:{COLOR_TEXTO}; font-size:0.9rem; line-height:1.5;'>
                {datos_comparable['descripcion']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_video:
        busqueda = datos_comparable["busqueda_youtube"].replace(" ", "+")
        st.markdown(f"""
        <a href="https://www.youtube.com/results?search_query={busqueda}" target="_blank"
           style="text-decoration:none;">
            <div style="background:#0d1b2a; border:2px solid {COLOR_ACENTO};
                 border-radius:8px; padding:40px; text-align:center; cursor:pointer;
                 transition:opacity 0.2s;">
                <div style="font-size:48px;">▶️</div>
                <div style="color:{COLOR_TEXTO}; font-size:1rem; margin-top:12px;
                     font-family:Oswald,sans-serif; letter-spacing:1px;">
                    Ver highlights de <strong style='color:{COLOR_ACENTO};'>
                    {nombre_comparable}</strong> en YouTube
                </div>
                <div style="color:{COLOR_GRIS}; font-size:0.78rem; margin-top:8px;">
                    YouTube API se integrará en la siguiente fase
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)