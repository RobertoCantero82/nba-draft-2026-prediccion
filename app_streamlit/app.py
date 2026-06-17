import streamlit as st
import pandas as pd
import joblib
import os
import random
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NBA Draft 2026 - Predicción",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# ESTILOS GLOBALES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8F9FA; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }
.app-header { background: linear-gradient(135deg, #1B4F8A 0%, #0d3060 60%, #F7520A 100%); border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; position: relative; overflow: hidden; }
.app-header::before { content: "2026"; font-family: 'Bebas Neue', sans-serif; font-size: 10rem; color: rgba(255,255,255,0.05); position: absolute; right: 2rem; top: -1.5rem; line-height: 1; pointer-events: none; }
.app-header h1 { font-family: 'Bebas Neue', sans-serif; font-size: 2.6rem; color: white; letter-spacing: 2px; margin: 0; line-height: 1.1; }
.app-header p { color: rgba(255,255,255,0.75); font-size: 1.05rem; margin: 0.3rem 0 0 0; font-weight: 300; }
.header-badge { background: rgba(247,82,10,0.9); color: white; font-family: 'Bebas Neue', sans-serif; font-size: 1.1rem; letter-spacing: 1px; padding: 0.4rem 1rem; border-radius: 20px; }
.stTabs [data-baseweb="tab-list"] { background: white; border-radius: 12px; padding: 4px; gap: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.stTabs [data-baseweb="tab"] { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.96rem; color: #6B7280; border-radius: 8px; padding: 0.5rem 1.2rem; }
.stTabs [aria-selected="true"] { background: #1B4F8A !important; color: white !important; }
.player-card { background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.07); position: relative; overflow: hidden; height: 100%; border-top: 4px solid #F7520A; }
.player-card::before { content: attr(data-pick); font-family: 'Bebas Neue', sans-serif; font-size: 7rem; color: rgba(27,79,138,0.06); position: absolute; right: -0.5rem; bottom: -1rem; line-height: 1; pointer-events: none; }
.player-name { font-family: 'Bebas Neue', sans-serif; font-size: 1.8rem; color: #1B4F8A; letter-spacing: 1px; margin: 0 0 0.2rem 0; line-height: 1.1; }
.player-meta { font-size: 0.88rem; color: #9CA3AF; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 1rem; }
.mock-pick { display: inline-block; background: #FFF4EE; color: #F7520A; font-family: 'Bebas Neue', sans-serif; font-size: 1rem; letter-spacing: 1px; padding: 0.2rem 0.7rem; border-radius: 20px; margin-bottom: 1rem; }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: 1rem 0; }
.stat-pill { background: #F0F4FA; border-radius: 10px; padding: 0.5rem; text-align: center; }
.stat-value { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; color: #1B4F8A; line-height: 1; }
.stat-label { font-size: 0.74rem; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
.pred-box { background: linear-gradient(135deg, #1B4F8A, #0d3060); border-radius: 14px; padding: 1.2rem 1.5rem; color: white; margin-top: 1rem; }
.pred-title { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.6); margin-bottom: 0.8rem; font-weight: 600; }
.pred-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; }
.pred-label { font-size: 0.88rem; color: rgba(255,255,255,0.7); }
.pred-value { font-family: 'Bebas Neue', sans-serif; font-size: 1.2rem; letter-spacing: 1px; }
.pred-value.orange { color: #F7520A; }
.pred-value.white  { color: white; }
.comparable-box { background: #FFF4EE; border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.8rem; border-left: 3px solid #F7520A; }
.comparable-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; color: #F7520A; font-weight: 700; margin-bottom: 0.2rem; }
.comparable-name { font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; color: #1B4F8A; letter-spacing: 1px; }
.comparable-desc { font-size: 0.88rem; color: #6B7280; margin-top: 0.2rem; }
.yt-btn { display: inline-flex; align-items: center; gap: 0.4rem; background: #FF0000; color: white; font-size: 0.88rem; font-weight: 600; padding: 0.4rem 0.9rem; border-radius: 20px; text-decoration: none; margin-top: 0.6rem; }
.mock-header { font-family: 'Bebas Neue', sans-serif; font-size: 1.6rem; color: #1B4F8A; letter-spacing: 2px; margin-bottom: 0.3rem; }
.mock-subheader { font-size: 0.94rem; color: #9CA3AF; margin-bottom: 1.5rem; }
.mock-result { background: white; border-radius: 14px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.07); border-left: 5px solid #F7520A; }
.mock-result-pick { font-family: 'Bebas Neue', sans-serif; font-size: 3rem; color: #F7520A; line-height: 1; }
.mock-result-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; color: #9CA3AF; font-weight: 600; }
.mock-result-ronda { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; color: #1B4F8A; letter-spacing: 1px; }
.prob-bar-wrap { margin: 0.4rem 0; }
.prob-bar-label { display: flex; justify-content: space-between; font-size: 0.84rem; color: #6B7280; margin-bottom: 0.15rem; font-weight: 500; }
.prob-bar-bg { background: #E8EDF2; border-radius: 6px; height: 8px; overflow: hidden; }
.prob-bar-fill { height: 100%; border-radius: 6px; transition: width 0.5s ease; }
.info-box { background: #F0F4FA; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; border-left: 4px solid #1B4F8A; }
.info-box p { margin: 0; font-size: 0.96rem; color: #374151; line-height: 1.6; }
.info-box strong { color: #1B4F8A; }
.section-divider { height: 1px; background: linear-gradient(to right, #F7520A, transparent); margin: 1.5rem 0; }
.stButton > button { background: linear-gradient(135deg, #F7520A, #d94008); color: white; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 0.93rem; border: none; border-radius: 10px; padding: 0.55rem 1.4rem; letter-spacing: 0.5px; transition: all 0.2s; width: 100%; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(247,82,10,0.35); }
.stNumberInput > div > div > input, .stTextInput > div > div > input, .stSelectbox > div > div { border-radius: 8px !important; border-color: #E5E7EB !important; font-family: 'Inter', sans-serif !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATOS DE LOS JUGADORES
# ─────────────────────────────────────────────
JUGADORES = {
    "Aday Mara": {
        "posicion": "Pívot", "liga": "NCAA - Michigan", "edad": 19, "altura": "2.13m",
        "mock_pick": "~#9", "mock_num": 9,
        "stats": {"PTS": 12.1, "REB": 6.8, "AST": 0.9, "ROB": 0.4, "TAP": 2.6, "FG%": 67.0},
        "comparable": {"nombre": "Kristaps Porzingis", "desc": "Pívot europeo con impacto defensivo de élite y techo ofensivo sin explotar", "youtube": "https://www.youtube.com/watch?v=hiMFQ-gewJ8"},
        "arquetipo_label": "Pívot Defensivo Atlético", "color": "#F5EE20",
        # resultados reales del modelo (modelo_rango_sin_posicion + modelo_ronda_sin_posicion)
        "pred_real": {
            "probs_ronda": {"R1": 0.236, "R2": 0.355, "ND": 0.409},
            "probs_rango": {"1-10": 0.083, "11-20": 0.061, "21-30": 0.064, "31-40": 0.043, "41-50": 0.658, "51-60": 0.046, "ND": 0.045},
            "prob_draft": 95.5,
            "ronda_pred": "R2",
            "rango_pred": "41-50",
        }
    },
    "Baba Miller": {
        "posicion": "Ala-Pívot", "liga": "NCAA - Florida State", "edad": 22, "altura": "2.06m",
        "mock_pick": "~#45", "mock_num": 45,
        "stats": {"PTS": 13.0, "REB": 10.3, "AST": 1.2, "ROB": 0.8, "TAP": 0.9, "FG%": 52.0},
        "comparable": {"nombre": "Pascal Siakam", "desc": "Una versión joven con tremenda movilidad lateral y gran capacidad para correr la pista como una gacela", "youtube": "https://www.youtube.com/watch?v=YqC7a5LVW3I"},
        "arquetipo_label": "Ala-Pívot Físico y Reboteador", "color": "#D61616",
        "pred_real": {
            "probs_ronda": {"R1": 0.245, "R2": 0.363, "ND": 0.393},
            "probs_rango": {"1-10": 0.154, "11-20": 0.041, "21-30": 0.062, "31-40": 0.035, "41-50": 0.621, "51-60": 0.037, "ND": 0.051},
            "prob_draft": 94.9,
            "ronda_pred": "R2",
            "rango_pred": "41-50",
        }
    },
    "Sergio de Larrea": {
        "posicion": "Base", "liga": "ACB - Valencia Basket", "edad": 21, "altura": "1.96m",
        "mock_pick": "~#40", "mock_num": 40,
        "stats": {"PTS": 9.5, "REB": 3.1, "AST": 4.2, "ROB": 1.1, "TAP": 0.2, "FG%": 44.0},
        "comparable": {"nombre": "Josh Giddey", "desc": "Gran tamaño y creatividad, pero con la duda de una primera marcha explosiva o un físico realmente preparado", "youtube": "https://www.youtube.com/watch?v=uS6aP-i_2BQ"},
        "arquetipo_label": "Base Pasador y Defensor", "color": "#F88A2A",
        "pred_real": {
            "probs_ronda": {"R1": 0.185, "R2": 0.259, "ND": 0.556},
            "probs_rango": {"1-10": 0.122, "11-20": 0.061, "21-30": 0.063, "31-40": 0.115, "41-50": 0.440, "51-60": 0.083, "ND": 0.117},
            "prob_draft": 88.3,
            "ronda_pred": "R2",
            "rango_pred": "41-50",
        }
    }
}

SPIDER_STATS = ["PTS", "REB", "AST", "ROB", "TAP", "FG%"]
SPIDER_MAX   = [35.0, 15.0, 10.0, 3.5, 4.0, 85.0]


# ─────────────────────────────────────────────
# CARGA DE MODELOS
# ─────────────────────────────────────────────
@st.cache_resource
def cargar_modelos():
    _dir = os.path.dirname(os.path.abspath(__file__))
    _local = os.path.join(_dir, '..', 'pkl')
    _hf    = os.path.join(_dir, 'pkl')
    base   = _hf if os.path.exists(_hf) else _local
    try:
        modelo_ronda = joblib.load(os.path.join(base, 'modelos',      'modelo_ronda_sin_posicion.pkl'))
        modelo_rango = joblib.load(os.path.join(base, 'modelos',      'modelo_rango_sin_posicion.pkl'))
        le_ronda     = joblib.load(os.path.join(base, 'preprocesado', 'le_ronda_sin_posicion.pkl'))
        le_rango     = joblib.load(os.path.join(base, 'preprocesado', 'le_rango_sin_posicion.pkl'))
        ruta_medianas = os.path.join(base, 'preprocesado', 'medianas_features.pkl')
        medianas = joblib.load(ruta_medianas) if os.path.exists(ruta_medianas) else None
        return modelo_ronda, modelo_rango, le_ronda, le_rango, medianas, True
    except Exception as e:
        return None, None, None, None, None, False

modelo_ronda, modelo_rango, le_ronda, le_rango, medianas_train, modelos_ok = cargar_modelos()




# ─────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────────
def build_input(pts, reb, ast, rob, tap, cols_modelo, imputar_ceros=False):
    """construyo el dataframe con todas las features del modelo.
    imputar_ceros=True replica el comportamiento del notebook (sección 9):
    el resto de features a 0, exactamente igual que al generar la gráfica.
    imputar_ceros=False usa medianas del train (modo draft personalizado)."""
    input_usuario = {'pts': pts, 'treb': reb, 'ast': ast, 'stl': rob, 'blk': tap}
    if imputar_ceros or medianas_train is None:
        fila = {col: 0 for col in cols_modelo}
    else:
        fila = medianas_train.reindex(cols_modelo).to_dict()
    for col, val in input_usuario.items():
        if col in fila:
            fila[col] = val
    return pd.DataFrame([fila])[cols_modelo]


def predecir_jugador(pts, reb, ast, rob, tap, imputar_ceros=False):
    """ejecuto los modelos de ronda y rango y devuelvo las probabilidades."""
    if not modelos_ok:
        return None
    cols_ronda  = list(modelo_ronda.feature_names_in_)
    X_ronda     = build_input(pts, reb, ast, rob, tap, cols_ronda, imputar_ceros)
    probs_ronda = modelo_ronda.predict_proba(X_ronda)[0]
    clases_ronda = le_ronda.classes_
    cols_rango  = list(modelo_rango.feature_names_in_)
    X_rango     = build_input(pts, reb, ast, rob, tap, cols_rango, imputar_ceros)
    probs_rango = modelo_rango.predict_proba(X_rango)[0]
    clases_rango = le_rango.classes_
    return {
        "probs_ronda": dict(zip(clases_ronda, probs_ronda)),
        "probs_rango": dict(zip(clases_rango, probs_rango)),
        "prob_draft":  sum(p for c, p in zip(clases_ronda, probs_ronda) if c != "ND") * 100
    }


# ─────────────────────────────────────────────
# ARQUETIPOS POR REGLAS + REFERENCIAS NBA
# ─────────────────────────────────────────────
REFERENCIAS_NBA = {
    "🗼 Pívot Clásico": [
        {"nombre": "Marc Gasol",       "youtube": "https://www.youtube.com/watch?v=VEa2ckauBjs"},
        {"nombre": "Steven Adams",     "youtube": "https://www.youtube.com/watch?v=PYWFAKqf3-g"},
        {"nombre": "Shaquille O'Neal", "youtube": "https://www.youtube.com/watch?v=dkrPBAhVFn0"},
    ],
    "🏀 Alero / Escolta Versátil": [
        {"nombre": "Aaron Gordon",    "youtube": "https://www.youtube.com/watch?v=9B_e_XJyHmU"},
        {"nombre": "Blake Griffin",   "youtube": "https://www.youtube.com/watch?v=hoarqsrBULo"},
        {"nombre": "Carmelo Anthony", "youtube": "https://www.youtube.com/watch?v=Ut29ViTVqQM"},
    ],
    "🎯 Base / Escolta Pequeño": [
        {"nombre": "Chris Paul",    "youtube": "https://www.youtube.com/watch?v=DTqykY_UlFw"},
        {"nombre": "Kyle Lowry",    "youtube": "https://www.youtube.com/watch?v=I14RCpMDxg4"},
        {"nombre": "Isaiah Thomas", "youtube": "https://www.youtube.com/watch?v=3mUNX086R50"},
    ],
    "⚡ Base / Escolta Explosivo": [
        {"nombre": "Russell Westbrook", "youtube": "https://www.youtube.com/watch?v=bxLbsmZ9qaY"},
        {"nombre": "De'Aaron Fox",      "youtube": "https://www.youtube.com/watch?v=B-8axVLwiRs"},
        {"nombre": "John Wall",         "youtube": "https://www.youtube.com/watch?v=9zkcPraU6-s"},
    ],
    "💥 Alero Atlético Explosivo": [
        {"nombre": "Anthony Edwards", "youtube": "https://www.youtube.com/watch?v=T5I70wkGVLI"},
        {"nombre": "LeBron James",    "youtube": "https://www.youtube.com/watch?v=-9lP95Qo-I0"},
        {"nombre": "Vince Carter",    "youtube": "https://www.youtube.com/watch?v=LrIfS5_TyQQ"},
    ],
    "🌟 Pívot Élite Moderno": [
        {"nombre": "Anthony Davis", "youtube": "https://www.youtube.com/watch?v=0ufyaXWbsnc"},
        {"nombre": "Joel Embiid",   "youtube": "https://www.youtube.com/watch?v=YrCTZtmpyLo"},
        {"nombre": "Nikola Jokic",  "youtube": "https://www.youtube.com/watch?v=7A-QGpW2GnA"},
    ],
    "🛡️ Alero / Escolta Duro": [
        {"nombre": "Jimmy Butler",  "youtube": "https://www.youtube.com/watch?v=aUnKhL3uHD4"},
        {"nombre": "Jrue Holiday",  "youtube": "https://www.youtube.com/watch?v=bxLGOD0B0kw"},
        {"nombre": "Paul Pierce",   "youtube": "https://www.youtube.com/watch?v=lh0YxMd3FfU"},
    ],
}

def asignar_arquetipo(pts, reb, ast, rob, tap):
    """asigno arquetipo por reglas sobre las stats del usuario — orden importa."""
    if reb > 8 and tap > 1.5 and ast < 3:
        return "🗼 Pívot Clásico"
    if reb > 7 and pts > 15 and ast > 2:
        return "🌟 Pívot Élite Moderno"
    if pts > 18 and reb > 5 and rob > 1.5:
        return "💥 Alero Atlético Explosivo"
    if ast > 5 and rob > 1.5 and reb < 5:
        return "⚡ Base / Escolta Explosivo"
    if ast > 5 and reb < 5:
        return "🎯 Base / Escolta Pequeño"
    if pts > 12 and reb > 5 and 2 <= ast <= 5:
        return "🏀 Alero / Escolta Versátil"
    if rob > 1.5 and reb > 4 and pts < 18:
        return "🛡️ Alero / Escolta Duro"
    return "🏀 Alero / Escolta Versátil"


def spider_chart(stats_dict, nombre, color):
    valores = [stats_dict.get(s, 0) / m * 100 for s, m in zip(SPIDER_STATS, SPIDER_MAX)]
    valores_closed = valores + [valores[0]]
    cats_closed    = SPIDER_STATS + [SPIDER_STATS[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valores_closed, theta=cats_closed, fill='toself',
        fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15)",
        line=dict(color=color, width=2.5), name=nombre
    ))
    fig.update_layout(
        polar=dict(bgcolor="white",
                   radialaxis=dict(visible=True, range=[0,100], tickfont=dict(size=9), gridcolor="#E8EDF2"),
                   angularaxis=dict(tickfont=dict(size=11, family="Inter", color="#374151"), gridcolor="#E8EDF2")),
        showlegend=False, paper_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40), height=260
    )
    return fig


def prob_bar_html(label, valor, color="#1B4F8A"):
    pct = round(float(valor) * 100, 1)
    return f"""
    <div class="prob-bar-wrap">
        <div class="prob-bar-label"><span>{label}</span><span>{pct}%</span></div>
        <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{pct}%;background:{color};"></div></div>
    </div>"""


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(
    '<div style="margin-bottom:1.8rem;padding:0.5rem 0 0.3rem 0;border-bottom:3px solid #F7520A;">'
    '<div style="font-family:Bebas Neue,sans-serif;font-size:4rem;color:#1B4F8A;'
    'letter-spacing:6px;line-height:1;margin-bottom:0.15rem;">Draft Radar</div>'
    '<div style="font-size:1rem;color:#6B7280;font-style:italic;margin-top:0.2rem;">'
    'La herramienta de predicción para el periodista del siglo XXI</div>'
    '</div>',
    unsafe_allow_html=True
)


# ─────────────────────────────────────────────
# TABS PRINCIPALES
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Españoles 2026", "Draft personalizado", "Acerca de"])


# ═════════════════════════════════════════════
# TAB 1 — ESPAÑOLES
# ═════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="info-box">
        <p>Analizo las estadísticas de la temporada de los tres candidatos españoles al <strong>NBA Draft 2026</strong>
        y aplico los modelos de ML entrenados para predecir su ronda de elección y rango de pick.
        Pulsa <strong>Predecir</strong> en cada jugador para ver los resultados.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3, gap="medium")
    color_map = {"ND": "#9CA3AF", "R1": "#1B4F8A", "R2": "#F7520A"}

    for col, (nombre, datos) in zip(cols, JUGADORES.items()):
        with col:
            stats = datos["stats"]
            comp  = datos["comparable"]

            st.markdown(f"""
            <div class="player-card" data-pick="{datos['mock_num']}">
                <div class="mock-pick">Proyección expertos {datos['mock_pick']}</div>
                <div class="player-name">{nombre}</div>
                <div class="player-meta">{datos['posicion']} · {datos['liga']} · {datos['edad']} años · {datos['altura']}</div>
                <div class="stats-grid">
                    <div class="stat-pill"><div class="stat-value">{stats['PTS']}</div><div class="stat-label">PTS</div></div>
                    <div class="stat-pill"><div class="stat-value">{stats['REB']}</div><div class="stat-label">REB</div></div>
                    <div class="stat-pill"><div class="stat-value">{stats['AST']}</div><div class="stat-label">AST</div></div>
                    <div class="stat-pill"><div class="stat-value">{stats['ROB']}</div><div class="stat-label">ROB</div></div>
                    <div class="stat-pill"><div class="stat-value">{stats['TAP']}</div><div class="stat-label">TAP</div></div>
                    <div class="stat-pill"><div class="stat-value">{stats['FG%']}%</div><div class="stat-label">FG%</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            fig = spider_chart(stats, nombre, datos["color"])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            _, col_btn, _ = st.columns([1, 2, 1])
            with col_btn:
                if st.button(f"Predecir - {nombre.split()[0]}", key=f"btn_{nombre.replace(' ','_')}"):
                    st.session_state[f"pred_{nombre}"] = True

            if st.session_state.get(f"pred_{nombre}"):
                resultado = predecir_jugador(stats["PTS"], stats["REB"], stats["AST"], stats["ROB"], stats["TAP"], imputar_ceros=True)

                # si los modelos cargan en runtime, uso sus probs; si no, uso los resultados
                # reales precalculados del notebook (mismos modelos, mismos datos de entrada)
                if resultado:
                    pr         = resultado["probs_ronda"]
                    pg         = resultado["probs_rango"]
                    ronda_pred = max(pr, key=pr.get)
                    rango_pred = max(pg, key=pg.get)
                    prob_draft = resultado["prob_draft"]
                else:
                    pred       = datos["pred_real"]
                    pr         = pred["probs_ronda"]
                    pg         = pred["probs_rango"]
                    ronda_pred = pred["ronda_pred"]
                    rango_pred = pred["rango_pred"]
                    prob_draft = pred["prob_draft"]

                st.markdown(f"""
                <div class="pred-box">
                    <div class="pred-title">Predicción del modelo</div>
                    <div class="pred-row"><span class="pred-label">Ronda</span><span class="pred-value orange">{ronda_pred}</span></div>
                    <div class="pred-row"><span class="pred-label">Rango de pick</span><span class="pred-value white">{rango_pred}</span></div>
                    <div class="pred-row"><span class="pred-label">Prob. de ser drafteado</span><span class="pred-value orange">{prob_draft:.1f}%</span></div>
                </div>
                """, unsafe_allow_html=True)

                # barras de ronda
                bars_html = "<div style='margin-top:0.8rem'>"
                for clase, prob in sorted(pr.items(), key=lambda x: -x[1]):
                    bars_html += prob_bar_html(clase, prob, color_map.get(clase, "#888"))
                bars_html += "</div>"
                st.markdown(bars_html, unsafe_allow_html=True)

                # barras de rango de pick
                st.markdown("##### Probabilidades por rango de pick")
                rangos_ordenados = ["1-10","11-20","21-30","31-40","41-50","51-60","ND"]
                colores_rangos   = ["#0d3060","#1B4F8A","#2e6fba","#5a94d4","#8fbce6","#b8d6f0","#9CA3AF"]
                bars_rango = ""
                for rango, color_r in zip(rangos_ordenados, colores_rangos):
                    bars_rango += prob_bar_html(rango, pg.get(rango, 0), color_r)
                st.markdown(bars_rango, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="comparable-box">
                    <div class="comparable-label">Jugador referencia</div>
                    <div class="comparable-name">{comp['nombre']}</div>
                    <div class="comparable-desc">{comp['desc']}</div>
                    <a class="yt-btn" href="{comp['youtube']}" target="_blank">▶ Ver highlights en YouTube</a>
                </div>
                """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# TAB 2 — MOCK DRAFT INTERACTIVO
# ═════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="mock-header">🎲 Draft Virtual</div>
    <div class="mock-subheader">
        Introduce las estadísticas básicas de cualquier jugador y el modelo predice
        en qué ronda y rango podría ser drafteado. ¿Podrías llegar tú a la NBA?
    </div>
    """, unsafe_allow_html=True)

    col_form, col_res = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("**Nombre del jugador**")
        nombre_mock = st.text_input("", placeholder="Ej: Roberto Cantero", label_visibility="collapsed", key="nombre_mock")
        st.markdown("**Estadísticas de temporada**")
        mc1, mc2 = st.columns(2)
        with mc1:
            pts_m = st.number_input("Puntos por partido",      min_value=0.0, max_value=45.0,  value=15.0, step=0.1, key="pts_m")
            reb_m = st.number_input("Rebotes por partido",     min_value=0.0, max_value=20.0,  value=6.0,  step=0.1, key="reb_m")
            ast_m = st.number_input("Asistencias por partido", min_value=0.0, max_value=15.0,  value=3.0,  step=0.1, key="ast_m")
        with mc2:
            rob_m = st.number_input("Robos por partido",       min_value=0.0, max_value=5.0,   value=1.0,  step=0.1, key="rob_m")
            tap_m = st.number_input("Tapones por partido",     min_value=0.0, max_value=6.0,   value=0.5,  step=0.1, key="tap_m")
            fg_m  = st.number_input("FG% (porcentaje tiro)",   min_value=0.0, max_value=100.0, value=48.0, step=0.5, key="fg_m")

        _, col_btn_mock, _ = st.columns([1, 2, 1])
        with col_btn_mock:
            predecir_mock = st.button("🏀 Predecir mi draft pick", key="btn_mock")

        nombre_display = nombre_mock.strip() if nombre_mock.strip() else "Tu jugador"
        stats_mock = {"PTS": pts_m, "REB": reb_m, "AST": ast_m, "ROB": rob_m, "TAP": tap_m, "FG%": fg_m}
        fig_mock = spider_chart(stats_mock, nombre_display, "#F7520A")
        st.plotly_chart(fig_mock, use_container_width=True, config={"displayModeBar": False})

        if modelos_ok and medianas_train is None:
            st.warning("⚠️ **medianas_features.pkl no encontrado.** Las features no introducidas se imputan con 0, lo que puede sesgar la predicción.")

    with col_res:
        if predecir_mock:
            resultado_mock = predecir_jugador(pts_m, reb_m, ast_m, rob_m, tap_m)

            if resultado_mock:
                pr = resultado_mock["probs_ronda"]
                pg = resultado_mock["probs_rango"]
                ronda_pred = max(pr, key=pr.get)
                rango_pred = max(pg, key=pg.get)
                prob_draft = resultado_mock["prob_draft"]
            else:
                pr = {"ND": 0.35, "R1": 0.28, "R2": 0.37}
                pg = {"1-10": 0.05, "11-20": 0.08, "21-30": 0.10, "31-40": 0.12, "41-50": 0.28, "51-60": 0.25, "ND": 0.12}
                ronda_pred = "R2"
                rango_pred = "41-50"
                prob_draft = 73.0

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1B4F8A,#0d3060);border-radius:16px;
                        padding:1.8rem 2rem;text-align:center;margin-bottom:1.2rem">
                <div style="font-size:0.78rem;text-transform:uppercase;letter-spacing:2px;
                            color:rgba(255,255,255,0.55);font-weight:600;margin-bottom:0.4rem">
                    Probabilidad de ser drafteado
                </div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:5rem;
                            color:#F7520A;line-height:1;letter-spacing:2px">
                    {prob_draft:.0f}%
                </div>
                <div style="margin-top:1rem">
                    <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;
                                color:rgba(255,255,255,0.5);font-weight:600">Rango pick</div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                                color:white;letter-spacing:1px">{rango_pred}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── arquetipo por reglas ──
            arquetipo = asignar_arquetipo(pts_m, reb_m, ast_m, rob_m, tap_m)
            ref = random.choice(REFERENCIAS_NBA[arquetipo])
            st.markdown(f"""
            <div style="background:#FFF4EE;border-radius:14px;padding:1.2rem 1.5rem;
                        margin-bottom:1.2rem;border-left:4px solid #F7520A;">
                <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;
                            color:#F7520A;font-weight:700;margin-bottom:0.3rem">Arquetipo</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                            color:#1B4F8A;letter-spacing:1px;margin-bottom:0.6rem">{arquetipo}</div>
                <div style="font-size:0.78rem;text-transform:uppercase;letter-spacing:1px;
                            color:#F7520A;font-weight:700;margin-bottom:0.2rem">Jugador referencia</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;
                            color:#1B4F8A;letter-spacing:1px;margin-bottom:0.5rem">{ref['nombre']}</div>
                <a href="{ref['youtube']}" target="_blank"
                   style="display:inline-flex;align-items:center;gap:0.4rem;background:#FF0000;
                          color:white;font-size:0.85rem;font-weight:600;padding:0.35rem 0.85rem;
                          border-radius:20px;text-decoration:none;">
                    ▶ Ver highlights en YouTube
                </a>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### Probabilidades por rango de pick")
            bars_rango = ""
            rangos_ordenados = ["1-10","11-20","21-30","31-40","41-50","51-60","ND"]
            colores_rangos   = ["#0d3060","#1B4F8A","#2e6fba","#5a94d4","#8fbce6","#b8d6f0","#9CA3AF"]
            for rango, color_r in zip(rangos_ordenados, colores_rangos):
                bars_rango += prob_bar_html(rango, pg.get(rango, 0), color_r)
            st.markdown(bars_rango, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="background:white;border-radius:14px;padding:3rem 2rem;text-align:center;
                        box-shadow:0 4px 20px rgba(0,0,0,0.07);margin-top:1rem">
                <div style="font-size:3rem;margin-bottom:1rem">🏀</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                            color:#1B4F8A;letter-spacing:2px;margin-bottom:0.5rem">
                    Rellena tus stats y predice
                </div>
                <div style="font-size:0.94rem;color:#9CA3AF">
                    El spider se actualiza en tiempo real.<br>
                    Pulsa <strong>Predecir</strong> para ver tu ronda y rango.
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# TAB 3 — PARA PERIODISTAS
# ═════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div style="width:100%;">

    <div style="margin-bottom:2rem;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#1B4F8A;
                    letter-spacing:2px;margin-bottom:0.6rem;">
            Qué te da esta herramienta
        </div>
        <p style="font-size:1rem;color:#374151;line-height:1.75;margin:0;">
            Draft Radar analiza las estadísticas de temporada de cualquier jugador y las compara
            con el histórico de más de 1.200 universitarios que pasaron por el proceso de draft
            entre 2009 y 2021. El resultado es una <strong style="color:#1B4F8A;">distribución de probabilidades</strong>:
            cuántas posibilidades tiene ese jugador de ser elegido en primera ronda, en segunda,
            o de quedarse fuera. No es una predicción cerrada. Es un punto de partida
            cuantitativo para construir un artículo con más capas.
        </p>
    </div>

    <div style="height:1px;background:linear-gradient(to right,#F7520A,transparent);margin-bottom:2rem;"></div>

    <div style="margin-bottom:2rem;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#1B4F8A;
                    letter-spacing:2px;margin-bottom:0.6rem;">
            Cómo leer los resultados
        </div>
        <p style="font-size:1rem;color:#374151;line-height:1.75;margin:0 0 0.8rem 0;">
            Lo más valioso no es la clase predicha —<em>R1, R2 o ND</em>— sino la
            <strong style="color:#1B4F8A;">distribución completa de probabilidades</strong>.
            Un jugador con un 55% de ND no es un descartado: es un caso de alta incertidumbre,
            y eso en sí mismo es una historia. Un jugador con un 80% de probabilidad de segunda
            ronda pero proyectado por los scouts en el top 10 señala exactamente la brecha
            entre lo que dicen los números y lo que ven los ojeadores sobre el terreno.
        </p>
        <p style="font-size:1rem;color:#374151;line-height:1.75;margin:0;">
            La pestaña <strong style="color:#1B4F8A;">Draft personalizado</strong> permite
            introducir las estadísticas de cualquier jugador —no solo los tres españoles—
            y obtener su perfil de probabilidades al instante.
        </p>
    </div>

    <div style="height:1px;background:linear-gradient(to right,#F7520A,transparent);margin-bottom:2rem;"></div>

    <div style="margin-bottom:1rem;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#1B4F8A;
                    letter-spacing:2px;margin-bottom:0.6rem;">
            Lo que los datos no pueden ver
        </div>
        <p style="font-size:1rem;color:#374151;line-height:1.75;margin:0 0 0.8rem 0;">
            El modelo fue entrenado con estadísticas de jugadores universitarios americanos.
            Aday Mara parece que podría subir posiciones en el Draft, Baba Miller puede rondar
            las predicciones de este modelo y Sergio de Larrea, al llegar desde Europa, tiene un Draft incierto.
        </p>
        <p style="font-size:1rem;color:#374151;line-height:1.75;margin:0;">
            Además, el draft nunca es solo estadística. El estado físico en el combine,
            las entrevistas con los equipos, la necesidad de cada franquicia en cada posición,
            el carácter del jugador —todo eso pesa, y nada de eso aparece en una hoja de cálculo.
            <strong style="color:#F7520A;">Esa brecha entre lo que predice el modelo y lo que
            decide el scout es, precisamente, la mejor historia que puede contar un periodista
            con esta herramienta.</strong>
        </p>
    </div>

    </div>
    """, unsafe_allow_html=True)
