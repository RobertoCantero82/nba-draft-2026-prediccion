import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NBA Draft 2026 · Españoles",
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
        modelo_ronda  = joblib.load(os.path.join(base, 'modelos', 'xgb_draft_balanceado.pkl'))
        modelo_rango  = joblib.load(os.path.join(base, 'modelos', 'xgb_rango_balanceado.pkl'))
        modelo_arq    = joblib.load(os.path.join(base, 'modelos', 'kmeans_arquetipos.pkl'))
        le_ronda      = joblib.load(os.path.join(base, 'preprocesado', 'le_target_draft.pkl'))
        le_rango      = joblib.load(os.path.join(base, 'preprocesado', 'le_rango.pkl'))
        return modelo_ronda, modelo_rango, modelo_arq, le_ronda, le_rango, True
    except Exception as e:
        return None, None, None, None, None, False

modelo_ronda, modelo_rango, modelo_arq, le_ronda, le_rango, modelos_ok = cargar_modelos()


# ─────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────────
def build_input(pts, reb, ast, rob, tap, fg_pct, tiene_posicion=False):
    """Construyo un dataframe con las estadísticas para pasarle al modelo."""
    data = {
        'pts': pts, 'treb': reb, 'ast': ast,
        'stl': rob, 'blk': tap, 'fg_pct': fg_pct
    }
    return pd.DataFrame([data])


def predecir_jugador(pts, reb, ast, rob, tap, fg_pct):
    """Ejecuto los tres modelos y devuelvo ronda, rango y arquetipo."""
    if not modelos_ok:
        return None

    X = build_input(pts, reb, ast, rob, tap, fg_pct)

    # --- ronda ---
    # reindexo para que las columnas coincidan con las del modelo entrenado
    cols_ronda = modelo_ronda.get_booster().feature_names
    X_ronda = X.reindex(columns=cols_ronda, fill_value=0)
    probs_ronda = modelo_ronda.predict_proba(X_ronda)[0]
    clases_ronda = le_ronda.classes_  # ['ND', 'R1', 'R2']

    # --- rango ---
    cols_rango = modelo_rango.get_booster().feature_names
    X_rango = X.reindex(columns=cols_rango, fill_value=0)
    probs_rango = modelo_rango.predict_proba(X_rango)[0]
    clases_rango = le_rango.classes_

    # --- arquetipo: uso solo stats físicas básicas ---
    try:
        X_arq = np.array([[pts, reb, ast, rob, tap]])
        arquetipo_id = modelo_arq.predict(X_arq)[0]
        arquetipos_nombres = [
            "Anotador Explosivo", "Ala-Pívot Físico", "Base Creativo",
            "Pívot Defensivo", "3&D Specialist", "Comodín Versátil"
        ]
        arquetipo_nombre = arquetipos_nombres[arquetipo_id % len(arquetipos_nombres)]
    except:
        arquetipo_nombre = "Perfil sin clasificar"

    return {
        "probs_ronda":  dict(zip(clases_ronda, probs_ronda)),
        "probs_rango":  dict(zip(clases_rango, probs_rango)),
        "arquetipo":    arquetipo_nombre,
        "prob_draft":   sum(p for c, p in zip(clases_ronda, probs_ronda) if c != "ND") * 100
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
    pct = round(valor * 100, 1)
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
st.markdown("""
<div class="app-header">
    <div>
        <h1>🏀 NBA Draft 2026<br>Predicción · Españoles</h1>
        <p>Machine Learning aplicado al draft — The Bridge Data Science Bootcamp</p>
    </div>
    <div class="header-badge">Draft · 26 Jun 2026</div>
</div>
""", unsafe_allow_html=True)


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
        <p>Analizo las estadísticas de temporada de los tres candidatos españoles al <strong>NBA Draft 2026</strong>
        y aplico los modelos de ML entrenados para predecir su ronda de elección, rango de pick y arquetipo de jugador.
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
                <div class="mock-pick">Mock consensus {datos['mock_pick']}</div>
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
            if st.button(f"🔮 Predecir · {nombre.split()[0]}", key=key_btn):
                st.session_state[f"pred_{nombre}"] = True

            # ── RESULTADO ──
            if st.session_state.get(f"pred_{nombre}"):
                resultado = predecir_jugador(
                    stats["PTS"], stats["REB"], stats["AST"],
                    stats["ROB"], stats["TAP"], stats["FG%"]
                )

                if resultado:
                    pr = resultado["probs_ronda"]
                    pg = resultado["probs_rango"]
                    ronda_pred  = max(pr, key=pr.get)
                    rango_pred  = max(pg, key=pg.get)
                    prob_draft  = resultado["prob_draft"]
                    arquetipo   = resultado["arquetipo"]

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
                            <span class="pred-label">P(ser drafteado)</span>
                            <span class="pred-value orange">{prob_draft:.1f}%</span>
                        </div>
                        <div class="pred-row">
                            <span class="pred-label">Arquetipo</span>
                            <span class="pred-value white" style="font-size:0.94rem">{arquetipo}</span>
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
                            <span class="pred-label">P(ser drafteado)</span>
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
    <div class="mock-header">🎲 Mock Draft · Tu Jugador</div>
    <div class="mock-subheader">
        Introduce las estadísticas básicas de cualquier jugador y el modelo predice
        en qué ronda y rango podría ser drafteado. ¿Cuánto vales tú en el draft?
    </div>
    """, unsafe_allow_html=True)

    col_form, col_res = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("**Nombre del jugador**")
        nombre_mock = st.text_input("", placeholder="Ej: Roberto Cantero", label_visibility="collapsed", key="nombre_mock")

        st.markdown("**Estadísticas de temporada**")
        mc1, mc2 = st.columns(2)
        with mc1:
            pts_m  = st.number_input("Puntos por partido",    min_value=0.0, max_value=45.0, value=15.0, step=0.1, key="pts_m")
            reb_m  = st.number_input("Rebotes por partido",   min_value=0.0, max_value=20.0, value=6.0,  step=0.1, key="reb_m")
            ast_m  = st.number_input("Asistencias por partido", min_value=0.0, max_value=15.0, value=3.0, step=0.1, key="ast_m")
        with mc2:
            rob_m  = st.number_input("Robos por partido",     min_value=0.0, max_value=5.0,  value=1.0,  step=0.1, key="rob_m")
            tap_m  = st.number_input("Tapones por partido",   min_value=0.0, max_value=6.0,  value=0.5,  step=0.1, key="tap_m")
            fg_m   = st.number_input("FG% (porcentaje tiro)", min_value=0.0, max_value=100.0, value=48.0, step=0.5, key="fg_m")

        predecir_mock = st.button("🏀 Predecir mi draft pick", key="btn_mock")

    with col_res:
        if predecir_mock:
            nombre_display = nombre_mock.strip() if nombre_mock.strip() else "Tu jugador"
            resultado_mock = predecir_jugador(pts_m, reb_m, ast_m, rob_m, tap_m, fg_m)

            if resultado_mock:
                pr = resultado_mock["probs_ronda"]
                pg = resultado_mock["probs_rango"]
                ronda_pred = max(pr, key=pr.get)
                rango_pred = max(pg, key=pg.get)
                prob_draft = resultado_mock["prob_draft"]
                arquetipo  = resultado_mock["arquetipo"]
            else:
                # demo fallback con los valores introducidos
                pr = {"ND": 0.35, "R1": 0.28, "R2": 0.37}
                pg = {"1-10": 0.05, "11-20": 0.08, "21-30": 0.10, "31-40": 0.12, "41-50": 0.28, "51-60": 0.25, "ND": 0.12}
                ronda_pred = "R2"
                rango_pred = "41-50"
                prob_draft = 73.0
                arquetipo  = "Ala-Pívot Físico"

            st.markdown(f"""
            <div class="mock-result">
                <div style="font-size:0.88rem;color:#9CA3AF;font-weight:600;text-transform:uppercase;
                            letter-spacing:1px;margin-bottom:0.5rem">Predicción para</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                            color:#1B4F8A;letter-spacing:2px;margin-bottom:1rem">{nombre_display}</div>
                <div style="display:flex;gap:2rem;margin-bottom:1rem">
                    <div>
                        <div class="mock-result-label">Ronda</div>
                        <div class="mock-result-ronda">{ronda_pred}</div>
                    </div>
                    <div>
                        <div class="mock-result-label">Rango pick</div>
                        <div class="mock-result-ronda">{rango_pred}</div>
                    </div>
                    <div>
                        <div class="mock-result-label">P(draft)</div>
                        <div class="mock-result-pick">{prob_draft:.0f}%</div>
                    </div>
                </div>
                <div style="background:#FFF4EE;border-radius:8px;padding:0.6rem 0.8rem;
                            display:inline-block;margin-bottom:1rem">
                    <span style="font-size:0.78rem;color:#F7520A;font-weight:700;
                                 text-transform:uppercase;letter-spacing:1px">Arquetipo · </span>
                    <span style="font-family:'Bebas Neue',sans-serif;color:#1B4F8A;
                                 font-size:1rem;letter-spacing:1px">{arquetipo}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### Probabilidades por ronda")
            bars_html = ""
            color_map = {"ND": "#9CA3AF", "R1": "#1B4F8A", "R2": "#F7520A"}
            for clase, prob in sorted(pr.items(), key=lambda x: -x[1]):
                bars_html += prob_bar_html(clase, prob, color_map.get(clase, "#888"))
            st.markdown(bars_html, unsafe_allow_html=True)

            st.markdown("##### Probabilidades por rango de pick")
            bars_rango = ""
            rangos_ordenados = ["1-10","11-20","21-30","31-40","41-50","51-60","ND"]
            colores_rangos = ["#0d3060","#1B4F8A","#2e6fba","#5a94d4","#8fbce6","#b8d6f0","#9CA3AF"]
            for rango, color_r in zip(rangos_ordenados, colores_rangos):
                prob_r = pg.get(rango, 0)
                bars_rango += prob_bar_html(rango, prob_r, color_r)
            st.markdown(bars_rango, unsafe_allow_html=True)

            # spider del jugador mock
            stats_mock = {"PTS": pts_m, "REB": reb_m, "AST": ast_m, "ROB": rob_m, "TAP": tap_m, "FG%": fg_m}
            fig_mock = spider_chart(stats_mock, nombre_display, "#F7520A")
            st.plotly_chart(fig_mock, use_container_width=True, config={"displayModeBar": False})

        else:
            st.markdown("""
            <div style="background:white;border-radius:14px;padding:3rem 2rem;text-align:center;
                        box-shadow:0 4px 20px rgba(0,0,0,0.07);margin-top:1rem">
                <div style="font-size:3rem;margin-bottom:1rem">🏀</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                            color:#1B4F8A;letter-spacing:2px;margin-bottom:0.5rem">
                    Introduce tus stats
                </div>
                <div style="font-size:0.94rem;color:#9CA3AF">
                    Rellena el formulario y pulsa <strong>Predecir</strong><br>
                    para descubrir en qué ronda serías elegido.
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# TAB 3 — CÓMO FUNCIONA
# ═════════════════════════════════════════════
with tab3:
    col_i1, col_i2 = st.columns(2, gap="large")

    with col_i1:
        st.markdown("""
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;
                    color:#1B4F8A;letter-spacing:2px;margin-bottom:1rem">
            Los Modelos
        </div>
        """, unsafe_allow_html=True)

        for titulo, texto in [
            ("Modelo de Ronda", "Predice si un jugador será elegido en primera ronda (R1), segunda ronda (R2) o no será drafteado (ND). Entrenado con datos de la NCAA 2009–2021 usando XGBoost con pesos balanceados para compensar el desbalanceo de clases."),
            ("Modelo de Rango", "Predice el rango de pick (1-10, 11-20... 51-60 o ND). Siete clases con un desbalanceo extremo — ND representa el 70% de los jugadores. El modelo aprende la diferencia entre rangos usando estadísticas de temporada."),
            ("Modelo de Arquetipo", "Clustering K-Means entrenado con datos del NBA Combine. Agrupa a los jugadores en perfiles tipo según sus medidas físicas y atléticas, y asigna el arquetipo más cercano al nuevo jugador."),
        ]:
            st.markdown(f"""
            <div class="info-box" style="margin-bottom:0.8rem">
                <p><strong>{titulo}</strong><br>{texto}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_i2:
        st.markdown("""
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;
                    color:#1B4F8A;letter-spacing:2px;margin-bottom:1rem">
            Limitaciones del Modelo
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box" style="border-left-color:#F7520A;margin-bottom:0.8rem">
            <p><strong>El dataset es de NCAA americana 2009–2021.</strong>
            Jugadores como Aday Mara (pivote europeo) o Sergio de Larrea (base de EuroLeague)
            no tienen precedente directo en el entrenamiento. El modelo predice a partir
            de las estadísticas numéricas, sin ver el contexto de liga ni el potencial físico.</p>
        </div>
        <div class="info-box" style="border-left-color:#F7520A;margin-bottom:0.8rem">
            <p><strong>Las probabilidades son más informativas que la clase predicha.</strong>
            Una predicción de ND con probabilidad 35% no significa "no será drafteado"
            — significa que el modelo tiene alta incertidumbre. La probabilidad combinada
            R1+R2 es la señal clave.</p>
        </div>
        <div class="info-box" style="border-left-color:#F7520A">
            <p><strong>El draft no es solo estadística.</strong>
            El consenso de scouts incorpora información que el modelo no tiene: trabajo de
            pre-draft, entrevistas con franquicias, atletismo, techo de desarrollo y
            necesidades específicas de cada equipo. Esta brecha entre ML y scouts
            es, en sí misma, el hallazgo más interesante del proyecto.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:linear-gradient(135deg,#1B4F8A,#0d3060);border-radius:14px;
                    padding:1.5rem;margin-top:1rem;color:white;text-align:center">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;
                        letter-spacing:2px;margin-bottom:0.5rem">Dataset de entrenamiento</div>
            <div style="display:flex;justify-content:space-around;margin-top:0.8rem">
                <div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;
                                color:#F7520A">~1.200</div>
                    <div style="font-size:0.78rem;color:rgba(255,255,255,0.6);
                                text-transform:uppercase;letter-spacing:1px">Jugadores</div>
                </div>
                <div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;
                                color:#F7520A">12</div>
                    <div style="font-size:0.78rem;color:rgba(255,255,255,0.6);
                                text-transform:uppercase;letter-spacing:1px">Temporadas NCAA</div>
                </div>
                <div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;
                                color:#F7520A">3</div>
                    <div style="font-size:0.78rem;color:rgba(255,255,255,0.6);
                                text-transform:uppercase;letter-spacing:1px">Modelos ML</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)