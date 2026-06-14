import streamlit as st
import pandas as pd
import joblib
import os
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

/* Reset y base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F8F9FA;
}

/* Ocultar elementos de streamlit */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }

/* ── HEADER ── */
.app-header {
    background: linear-gradient(135deg, #1B4F8A 0%, #0d3060 60%, #F7520A 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: "2026";
    font-family: 'Bebas Neue', sans-serif;
    font-size: 10rem;
    color: rgba(255,255,255,0.05);
    position: absolute;
    right: 2rem;
    top: -1.5rem;
    line-height: 1;
    pointer-events: none;
}
.app-header h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    color: white;
    letter-spacing: 2px;
    margin: 0;
    line-height: 1.1;
}
.app-header p {
    color: rgba(255,255,255,0.75);
    font-size: 1.05rem;
    margin: 0.3rem 0 0 0;
    font-weight: 300;
}
.header-badge {
    background: rgba(247,82,10,0.9);
    color: white;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 1px;
    padding: 0.4rem 1rem;
    border-radius: 20px;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.96rem;
    color: #6B7280;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: #1B4F8A !important;
    color: white !important;
}

/* ── PLAYER CARD ── */
.player-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    position: relative;
    overflow: hidden;
    height: 100%;
    border-top: 4px solid #F7520A;
}
.player-card::before {
    content: attr(data-pick);
    font-family: 'Bebas Neue', sans-serif;
    font-size: 7rem;
    color: rgba(27,79,138,0.06);
    position: absolute;
    right: -0.5rem;
    bottom: -1rem;
    line-height: 1;
    pointer-events: none;
}
.player-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: #1B4F8A;
    letter-spacing: 1px;
    margin: 0 0 0.2rem 0;
    line-height: 1.1;
}
.player-meta {
    font-size: 0.88rem;
    color: #9CA3AF;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
}
.mock-pick {
    display: inline-block;
    background: #FFF4EE;
    color: #F7520A;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 1px;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}

/* ── STAT PILLS ── */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin: 1rem 0;
}
.stat-pill {
    background: #F0F4FA;
    border-radius: 10px;
    padding: 0.5rem;
    text-align: center;
}
.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: #1B4F8A;
    line-height: 1;
}
.stat-label {
    font-size: 0.74rem;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}

/* ── RESULTADO PREDICCIÓN ── */
.pred-box {
    background: linear-gradient(135deg, #1B4F8A, #0d3060);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    color: white;
    margin-top: 1rem;
}
.pred-title {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 0.8rem;
    font-weight: 600;
}
.pred-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}
.pred-label {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.7);
}
.pred-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 1px;
}
.pred-value.orange { color: #F7520A; }
.pred-value.white  { color: white; }

/* ── COMPARABLE ── */
.comparable-box {
    background: #FFF4EE;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
    border-left: 3px solid #F7520A;
}
.comparable-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #F7520A;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.comparable-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    color: #1B4F8A;
    letter-spacing: 1px;
}
.comparable-desc {
    font-size: 0.88rem;
    color: #6B7280;
    margin-top: 0.2rem;
}

/* ── BOTÓN YOUTUBE ── */
.yt-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #FF0000;
    color: white;
    font-size: 0.88rem;
    font-weight: 600;
    padding: 0.4rem 0.9rem;
    border-radius: 20px;
    text-decoration: none;
    margin-top: 0.6rem;
}

/* ── MOCK DRAFT ── */
.mock-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #1B4F8A;
    letter-spacing: 2px;
    margin-bottom: 0.3rem;
}
.mock-subheader {
    font-size: 0.94rem;
    color: #9CA3AF;
    margin-bottom: 1.5rem;
}
.mock-result {
    background: white;
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    border-left: 5px solid #F7520A;
}
.mock-result-pick {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: #F7520A;
    line-height: 1;
}
.mock-result-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #9CA3AF;
    font-weight: 600;
}
.mock-result-ronda {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: #1B4F8A;
    letter-spacing: 1px;
}

/* ── PROB BAR ── */
.prob-bar-wrap { margin: 0.4rem 0; }
.prob-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.84rem;
    color: #6B7280;
    margin-bottom: 0.15rem;
    font-weight: 500;
}
.prob-bar-bg {
    background: #E8EDF2;
    border-radius: 6px;
    height: 8px;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.5s ease;
}

/* ── INFO BOX ── */
.info-box {
    background: #F0F4FA;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #1B4F8A;
}
.info-box p { margin: 0; font-size: 0.96rem; color: #374151; line-height: 1.6; }
.info-box strong { color: #1B4F8A; }

/* ── DIVIDER ── */
.section-divider {
    height: 1px;
    background: linear-gradient(to right, #F7520A, transparent);
    margin: 1.5rem 0;
}

/* Botones streamlit */
.stButton > button {
    background: linear-gradient(135deg, #F7520A, #d94008);
    color: white;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 0.93rem;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.4rem;
    letter-spacing: 0.5px;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(247,82,10,0.35);
}

/* Inputs */
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 8px !important;
    border-color: #E5E7EB !important;
    font-family: 'Inter', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATOS DE LOS JUGADORES
# ─────────────────────────────────────────────
JUGADORES = {
    "Aday Mara": {
        "posicion": "Pívot",
        "liga": "NCAA - Michigan",
        "edad": 19,
        "altura": "2.13m",
        "mock_pick": "~#9",
        "mock_num": 9,
        "stats": {"PTS": 12.1, "REB": 6.8, "AST": 0.9, "ROB": 0.4, "TAP": 2.6, "FG%": 67.0},
        "comparable": {
            "nombre": "Kristaps Porzingis",
            "desc": "Pívot europeo con impacto defensivo de élite y techo ofensivo sin explotar",
            "youtube": "https://www.youtube.com/watch?v=hiMFQ-gewJ8"
        },
        "arquetipo_label": "Pívot Defensivo Atlético",
        "color": "#F5EE20"
    },
    "Baba Miller": {
        "posicion": "Ala-Pívot",
        "liga": "NCAA - Florida State",
        "edad": 22,
        "altura": "2.06m",
        "mock_pick": "~#45",
        "mock_num": 45,
        "stats": {"PTS": 13.0, "REB": 10.3, "AST": 1.2, "ROB": 0.8, "TAP": 0.9, "FG%": 52.0},
        "comparable": {
            "nombre": "Pascal Siakam",
            "desc": "Una versión joven con tremenda movilidad lateral y gran capacidad para correr la pista como una gacela",
            "youtube": "https://www.youtube.com/watch?v=YqC7a5LVW3I"
        },
        "arquetipo_label": "Ala-Pívot Físico y Reboteador",
        "color": "#D61616"
    },
    "Sergio de Larrea": {
        "posicion": "Base",
        "liga": "ACB - Valencia Basket",
        "edad": 21,
        "altura": "1.96m",
        "mock_pick": "~#40",
        "mock_num": 40,
        "stats": {"PTS": 9.5, "REB": 3.1, "AST": 4.2, "ROB": 1.1, "TAP": 0.2, "FG%": 44.0},
        "comparable": {
            "nombre": "Josh Giddey",
            "desc": "Gran tamaño y creatividad, pero con la duda de una primera marcha explosiva o un físico realmente preparado",
            "youtube": "https://www.youtube.com/watch?v=uS6aP-i_2BQ"
        },
        "arquetipo_label": "Base Pasador y Defensor",
        "color": "#F88A2A"
    }
}

# Estadísticas para el spider (máximos de referencia NCAA)
SPIDER_STATS  = ["PTS", "REB", "AST", "ROB", "TAP", "FG%"]
SPIDER_MAX    = [35.0, 15.0, 10.0, 3.5, 4.0, 85.0]


# ─────────────────────────────────────────────
# CARGA DE MODELOS
# ─────────────────────────────────────────────
@st.cache_resource
def cargar_modelos():
    # cargo los modelos guardados en pkl — uso rutas relativas desde app_streamlit/
    base = os.path.join(os.path.dirname(__file__), '..', 'pkl')
    try:
        modelo_ronda  = joblib.load(os.path.join(base, 'modelos',      'modelo_ronda_sin_posicion.pkl'))
        modelo_rango  = joblib.load(os.path.join(base, 'modelos',      'modelo_rango_sin_posicion.pkl'))
        le_ronda      = joblib.load(os.path.join(base, 'preprocesado', 'le_ronda_sin_posicion.pkl'))
        le_rango      = joblib.load(os.path.join(base, 'preprocesado', 'le_rango_sin_posicion.pkl'))
        return modelo_ronda, modelo_rango, le_ronda, le_rango, True
    except Exception as e:
        return None, None, None, None, False

modelo_ronda, modelo_rango, le_ronda, le_rango, modelos_ok = cargar_modelos()


# ─────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────────
def build_input(pts, reb, ast, rob, tap):
    """Construyo un dataframe con las cinco estadísticas que usan los modelos sin posición."""
    data = {'pts': pts, 'treb': reb, 'ast': ast, 'stl': rob, 'blk': tap}
    return pd.DataFrame([data])


def predecir_jugador(pts, reb, ast, rob, tap):
    """Ejecuto los modelos de ronda y rango y devuelvo las probabilidades."""
    if not modelos_ok:
        return None

    X = build_input(pts, reb, ast, rob, tap)

    # --- ronda (Random Forest sin posición — 34 variables) ---
    # reindexo para que las columnas coincidan con las del modelo entrenado
    cols_ronda = list(modelo_ronda.feature_names_in_)
    X_ronda = X.reindex(columns=cols_ronda, fill_value=0)
    probs_ronda = modelo_ronda.predict_proba(X_ronda)[0]
    clases_ronda = le_ronda.classes_  # ['ND', 'R1', 'R2']

    # --- rango (XGBoost sin posición — 34 variables) ---
    cols_rango = list(modelo_rango.feature_names_in_)
    X_rango = X.reindex(columns=cols_rango, fill_value=0)
    probs_rango = modelo_rango.predict_proba(X_rango)[0]
    clases_rango = le_rango.classes_

    return {
        "probs_ronda": dict(zip(clases_ronda, probs_ronda)),
        "probs_rango": dict(zip(clases_rango, probs_rango)),
        "prob_draft":  sum(p for c, p in zip(clases_ronda, probs_ronda) if c != "ND") * 100
    }


def spider_chart(stats_dict, nombre, color):
    """Creo un gráfico radar con las estadísticas del jugador."""
    valores = [stats_dict.get(s, 0) / m * 100
               for s, m in zip(SPIDER_STATS, SPIDER_MAX)]
    valores_closed = valores + [valores[0]]
    cats_closed = SPIDER_STATS + [SPIDER_STATS[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valores_closed,
        theta=cats_closed,
        fill='toself',
        fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15)",
        line=dict(color=color, width=2.5),
        name=nombre
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="white",
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9), gridcolor="#E8EDF2"),
            angularaxis=dict(tickfont=dict(size=11, family="Inter", color="#374151"), gridcolor="#E8EDF2")
        ),
        showlegend=False,
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40),
        height=260
    )
    return fig


def prob_bar_html(label, valor, color="#1B4F8A"):
    """Genero una barra de probabilidad en HTML."""
    pct = round(float(valor) * 100, 1)
    return f"""
    <div class="prob-bar-wrap">
        <div class="prob-bar-label"><span>{label}</span><span>{pct}%</span></div>
        <div class="prob-bar-bg">
            <div class="prob-bar-fill" style="width:{pct}%;background:{color};"></div>
        </div>
    </div>"""


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
_header_html = (
    '<div style="background:linear-gradient(135deg,#1B4F8A 0%,#0d3060 55%,#c94a0a 100%);'
    'border-radius:16px;padding:0;margin-bottom:1.5rem;height:110px;position:relative;'
    'overflow:hidden;display:flex;align-items:stretch;">'

    '<div style="font-family:Bebas Neue,sans-serif;font-size:9rem;color:rgba(247,82,10,0.18);'
    'position:absolute;right:1.5rem;top:50%;transform:translateY(-50%);line-height:1;'
    'pointer-events:none;letter-spacing:-2px;">2026</div>'

    '<div style="display:flex;flex-direction:column;justify-content:center;'
    'padding:0 2rem;min-width:300px;z-index:2;">'
    '<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.1rem">'
    '<span style="font-size:1.6rem">&#127919;</span>'
    '<span style="font-family:Bebas Neue,sans-serif;font-size:2.4rem;color:white;'
    'letter-spacing:4px;line-height:1;">DraftRadar</span>'
    '</div>'
    '<div style="font-family:Bebas Neue,sans-serif;font-size:0.95rem;'
    'color:rgba(255,255,255,0.65);letter-spacing:2.5px;margin-bottom:0.25rem;">'
    'NBA DRAFT 2026 &middot; CANDIDATOS ESPA&Ntilde;OLES</div>'
    '<div style="font-size:0.78rem;color:rgba(255,255,255,0.45);letter-spacing:0.3px;">'
    'Machine Learning aplicado al draft &mdash; The Bridge Data Science Bootcamp</div>'
    '</div>'

    '<div style="flex:1;display:flex;align-items:center;justify-content:center;'
    'gap:2rem;z-index:2;padding:0 1rem;">'

    '<div style="display:flex;flex-direction:column;align-items:center;gap:0.4rem">'
    '<div style="font-family:Bebas Neue,sans-serif;font-size:0.8rem;color:white;letter-spacing:2px;">ADAY MARA</div>'
    '<div style="width:46px;height:62px;background:rgba(255,255,255,0.08);border-radius:8px;'
    'border:1.5px solid rgba(255,255,255,0.2);display:flex;flex-direction:column;'
    'align-items:center;justify-content:center;gap:2px;">'
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="rgba(255,255,255,0.7)">'
    '<path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12z"/>'
    '<path d="M12 14.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>'
    '</svg>'
    '<span style="font-family:Bebas Neue,sans-serif;font-size:0.95rem;color:#F7520A;line-height:1;">#9</span>'
    '</div>'
    '</div>'

    '<div style="display:flex;flex-direction:column;align-items:center;gap:0.4rem">'
    '<div style="font-family:Bebas Neue,sans-serif;font-size:0.8rem;color:white;letter-spacing:2px;">BABA MILLER</div>'
    '<div style="width:46px;height:62px;background:rgba(255,255,255,0.08);border-radius:8px;'
    'border:1.5px solid rgba(255,255,255,0.2);display:flex;flex-direction:column;'
    'align-items:center;justify-content:center;gap:2px;">'
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="rgba(255,255,255,0.7)">'
    '<path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12z"/>'
    '<path d="M12 14.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>'
    '</svg>'
    '<span style="font-family:Bebas Neue,sans-serif;font-size:0.95rem;color:#F7520A;line-height:1;">#45</span>'
    '</div>'
    '</div>'

    '<div style="display:flex;flex-direction:column;align-items:center;gap:0.4rem">'
    '<div style="font-family:Bebas Neue,sans-serif;font-size:0.8rem;color:white;letter-spacing:2px;">SERGIO DE LARREA</div>'
    '<div style="width:46px;height:62px;background:rgba(255,255,255,0.08);border-radius:8px;'
    'border:1.5px solid rgba(255,255,255,0.2);display:flex;flex-direction:column;'
    'align-items:center;justify-content:center;gap:2px;">'
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="rgba(255,255,255,0.7)">'
    '<path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12z"/>'
    '<path d="M12 14.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>'
    '</svg>'
    '<span style="font-family:Bebas Neue,sans-serif;font-size:0.95rem;color:#F7520A;line-height:1;">#40</span>'
    '</div>'
    '</div>'

    '</div>'
    '</div>'
)
st.markdown(_header_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS PRINCIPALES
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Españoles 2026",
    "Draft personalizado",
    "Funcionamiento del predictor"
])


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

    for col, (nombre, datos) in zip(cols, JUGADORES.items()):
        with col:
            stats = datos["stats"]
            comp  = datos["comparable"]

            # ── CARD ──
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

            # ── SPIDER ──
            fig = spider_chart(stats, nombre, datos["color"])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # ── BOTÓN PREDECIR ──
            key_btn = f"btn_{nombre.replace(' ','_')}"
            _, col_btn, _ = st.columns([1, 2, 1])
            with col_btn:
                if st.button(f"Predecir - {nombre.split()[0]}", key=key_btn):
                    st.session_state[f"pred_{nombre}"] = True

            # ── RESULTADO ──
            if st.session_state.get(f"pred_{nombre}"):
                resultado = predecir_jugador(
                    stats["PTS"], stats["REB"], stats["AST"],
                    stats["ROB"], stats["TAP"]
                )

                if resultado:
                    pr = resultado["probs_ronda"]
                    pg = resultado["probs_rango"]
                    ronda_pred  = max(pr, key=pr.get)
                    rango_pred  = max(pg, key=pg.get)
                    prob_draft  = resultado["prob_draft"]
                    arquetipo   = datos["arquetipo_label"]

                    # caja de resultado
                    st.markdown(f"""
                    <div class="pred-box">
                        <div class="pred-title">Predicción del modelo</div>
                        <div class="pred-row">
                            <span class="pred-label">Ronda</span>
                            <span class="pred-value orange">{ronda_pred}</span>
                        </div>
                        <div class="pred-row">
                            <span class="pred-label">Rango de pick</span>
                            <span class="pred-value white">{rango_pred}</span>
                        </div>
                        <div class="pred-row">
                            <span class="pred-label">Prob. de ser drafteado</span>
                            <span class="pred-value orange">{prob_draft:.1f}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # barras de probabilidad por ronda
                    bars_html = "<div style='margin-top:0.8rem'>"
                    color_map = {"ND": "#9CA3AF", "R1": "#1B4F8A", "R2": "#F7520A"}
                    for clase, prob in sorted(pr.items(), key=lambda x: -x[1]):
                        bars_html += prob_bar_html(clase, prob, color_map.get(clase, "#888"))
                    bars_html += "</div>"
                    st.markdown(bars_html, unsafe_allow_html=True)

                else:
                    # modo demo si no hay modelos cargados
                    probs_demo = {"ND": 0.354, "R1": 0.253, "R2": 0.393}
                    ronda_demo = "R2"
                    st.markdown(f"""
                    <div class="pred-box">
                        <div class="pred-title">Predicción del modelo · Demo</div>
                        <div class="pred-row">
                            <span class="pred-label">Ronda</span>
                            <span class="pred-value orange">{ronda_demo}</span>
                        </div>
                        <div class="pred-row">
                            <span class="pred-label">Rango de pick</span>
                            <span class="pred-value white">41-50</span>
                        </div>
                        <div class="pred-row">
                            <span class="pred-label">Prob. de ser drafteado</span>
                            <span class="pred-value orange">64.6%</span>
                        </div>
                        <div class="pred-row">
                            <span class="pred-label">Arquetipo</span>
                            <span class="pred-value white" style="font-size:0.94rem">{datos['arquetipo_label']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    bars_html = "<div style='margin-top:0.8rem'>"
                    for clase, prob in sorted(probs_demo.items(), key=lambda x: -x[1]):
                        bars_html += prob_bar_html(clase, prob, color_map.get(clase,"#888"))
                    bars_html += "</div>"
                    st.markdown(bars_html, unsafe_allow_html=True)

                # ── COMPARABLE ──
                st.markdown(f"""
                <div class="comparable-box">
                    <div class="comparable-label">Jugador referencia</div>
                    <div class="comparable-name">{comp['nombre']}</div>
                    <div class="comparable-desc">{comp['desc']}</div>
                    <a class="yt-btn" href="{comp['youtube']}" target="_blank">
                        ▶ Ver highlights en YouTube
                    </a>
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

    # ── COLUMNA IZQUIERDA: formulario + spider (siempre visible) ──
    with col_form:
        st.markdown("**Nombre del jugador**")
        nombre_mock = st.text_input("", placeholder="Ej: Roberto Cantero", label_visibility="collapsed", key="nombre_mock")

        st.markdown("**Estadísticas de temporada**")
        mc1, mc2 = st.columns(2)
        with mc1:
            pts_m  = st.number_input("Puntos por partido",      min_value=0.0, max_value=45.0,  value=15.0, step=0.1, key="pts_m")
            reb_m  = st.number_input("Rebotes por partido",     min_value=0.0, max_value=20.0,  value=6.0,  step=0.1, key="reb_m")
            ast_m  = st.number_input("Asistencias por partido", min_value=0.0, max_value=15.0,  value=3.0,  step=0.1, key="ast_m")
        with mc2:
            rob_m  = st.number_input("Robos por partido",       min_value=0.0, max_value=5.0,   value=1.0,  step=0.1, key="rob_m")
            tap_m  = st.number_input("Tapones por partido",     min_value=0.0, max_value=6.0,   value=0.5,  step=0.1, key="tap_m")
            fg_m   = st.number_input("FG% (porcentaje tiro)",   min_value=0.0, max_value=100.0, value=48.0, step=0.5, key="fg_m")

        # botón centrado
        _, col_btn_mock, _ = st.columns([1, 2, 1])
        with col_btn_mock:
            predecir_mock = st.button("🏀 Predecir mi draft pick", key="btn_mock")

        # spider: siempre visible, se actualiza en tiempo real con los inputs
        nombre_display = nombre_mock.strip() if nombre_mock.strip() else "Tu jugador"
        stats_mock = {"PTS": pts_m, "REB": reb_m, "AST": ast_m, "ROB": rob_m, "TAP": tap_m, "FG%": fg_m}
        fig_mock = spider_chart(stats_mock, nombre_display, "#F7520A")
        st.plotly_chart(fig_mock, use_container_width=True, config={"displayModeBar": False})

    # ── COLUMNA DERECHA: resultados tras pulsar Predecir ──
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
                # demo fallback
                pr = {"ND": 0.35, "R1": 0.28, "R2": 0.37}
                pg = {"1-10": 0.05, "11-20": 0.08, "21-30": 0.10, "31-40": 0.12, "41-50": 0.28, "51-60": 0.25, "ND": 0.12}
                ronda_pred = "R2"
                rango_pred = "41-50"
                prob_draft = 73.0

            # ── bloque P(draft) destacado ──
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
                <div style="display:flex;justify-content:center;gap:2.5rem;margin-top:1rem">
                    <div>
                        <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;
                                    color:rgba(255,255,255,0.5);font-weight:600">Ronda</div>
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                                    color:white;letter-spacing:1px">{ronda_pred}</div>
                    </div>
                    <div style="width:1px;background:rgba(255,255,255,0.15)"></div>
                    <div>
                        <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;
                                    color:rgba(255,255,255,0.5);font-weight:600">Rango pick</div>
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                                    color:white;letter-spacing:1px">{rango_pred}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── barras de probabilidad por ronda ──
            st.markdown("##### Probabilidades por ronda")
            bars_html = ""
            color_map = {"ND": "#9CA3AF", "R1": "#1B4F8A", "R2": "#F7520A"}
            for clase, prob in sorted(pr.items(), key=lambda x: -x[1]):
                bars_html += prob_bar_html(clase, prob, color_map.get(clase, "#888"))
            st.markdown(bars_html, unsafe_allow_html=True)

            # ── barras de probabilidad por rango ──
            st.markdown("##### Probabilidades por rango de pick")
            bars_rango = ""
            rangos_ordenados = ["1-10","11-20","21-30","31-40","41-50","51-60","ND"]
            colores_rangos = ["#0d3060","#1B4F8A","#2e6fba","#5a94d4","#8fbce6","#b8d6f0","#9CA3AF"]
            for rango, color_r in zip(rangos_ordenados, colores_rangos):
                prob_r = pg.get(rango, 0)
                bars_rango += prob_bar_html(rango, prob_r, color_r)
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
# TAB 3 — CÓMO FUNCIONA
# ═════════════════════════════════════════════
with tab3:
    c3a, c3b, c3c = st.columns(3, gap="large")

    with c3a:
        st.markdown("""
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;
                    color:#1B4F8A;letter-spacing:2px;margin-bottom:0.8rem">⚙️ Los modelos</div>
        <div class="info-box" style="margin-bottom:0.6rem">
            <p><strong>Ronda</strong> (Random Forest)<br>
            R1 / R2 / ND. Entrenado con NCAA 2009–2021. F1 macro 0.60.</p>
        </div>
        <div class="info-box" style="margin-bottom:0.6rem">
            <p><strong>Rango de pick</strong> (XGBoost)<br>
            7 clases: 1-10 hasta 51-60 + ND. F1 macro 0.23 — techo estructural del problema.</p>
        </div>
        <div class="info-box">
            <p><strong>Arquetipo</strong> (K-Means k=7)<br>
            Entrenado con datos del NBA Combine: altura, peso, envergadura, salto y agilidad.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3b:
        st.markdown("""
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;
                    color:#1B4F8A;letter-spacing:2px;margin-bottom:0.8rem">⚠️ Limitaciones</div>
        <div class="info-box" style="border-left-color:#F7520A;margin-bottom:0.6rem">
            <p><strong>Dataset NCAA americano.</strong> Los tres candidatos son europeos sin
            precedente directo en el entrenamiento. El modelo solo ve estadísticas numéricas.</p>
        </div>
        <div class="info-box" style="border-left-color:#F7520A">
            <p><strong>Probabilidad, no certeza.</strong> La distribución R1+R2+ND es
            la señal clave, no la clase predicha. Un 35% de ND indica incertidumbre alta,
            no descarte.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3c:
        st.markdown("""
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;
                    color:#1B4F8A;letter-spacing:2px;margin-bottom:0.8rem">📊 El dataset</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1B4F8A,#0d3060);border-radius:14px;
                    padding:1.5rem;color:white;text-align:center;margin-bottom:0.6rem">
            <div style="display:flex;justify-content:space-around">
                <div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#F7520A">~1.200</div>
                    <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:1px">jugadores</div>
                </div>
                <div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#F7520A">12</div>
                    <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:1px">temporadas</div>
                </div>
                <div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#F7520A">34</div>
                    <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:1px">variables</div>
                </div>
            </div>
        </div>
        <div class="info-box" style="border-left-color:#F7520A">
            <p><strong>El draft no es solo estadística.</strong> Scouts, entrevistas,
            atletismo y necesidades de cada equipo son información que el modelo no tiene.
            Esa brecha ML–scouts es el hallazgo más interesante del proyecto.</p>
        </div>
        """, unsafe_allow_html=True)