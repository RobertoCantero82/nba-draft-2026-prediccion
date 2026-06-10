import streamlit as st
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="NBA Draft 2026 · Predictor",
    page_icon="🏀",
    layout="wide",
)

st.markdown("""
<style>
.block-container { padding: 2rem 2.5rem; }
h1 { font-size: 1.8rem; font-weight: 700; margin-bottom: 0; }
.subtitulo { color: #64748b; font-size: 0.9rem; margin-top: 2px; margin-bottom: 1.5rem; }
.resultado-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
}
.res-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;
             letter-spacing: 0.1em; margin-bottom: 2px; }
.res-valor { font-size: 1.6rem; font-weight: 700; line-height: 1.1; }
.res-pct   { font-size: 0.78rem; color: #64748b; margin-top: 2px; }
.comp-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
}
.comp-nombre { font-size: 1rem; font-weight: 600; }
.comp-detalle { font-size: 0.8rem; color: #64748b; margin-top: 2px; }
.divider { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Datos ────────────────────────────────────────────────────────────────────

ARQUETIPOS = {
    "C":  "Pívot clásico",
    "PF": "Pívot élite moderno",
    "SF": "Alero atlético",
    "SG": "Alero versátil",
    "PG": "Base explosivo",
}

COMPARABLES = {
    "C":  ("Kristaps Porziņģis",       "Pick #4 · 2015 · Pívot · 213 cm",        "Kristaps Porzingis NBA highlights"),
    "PF": ("Pau Gasol",                 "Pick #3 · 2001 · Ala-pívot · 213 cm",    "Pau Gasol NBA highlights"),
    "SF": ("Rudy Gay",                  "Pick #8 · 2006 · Alero · 203 cm",         "Rudy Gay NBA highlights"),
    "SG": ("Devin Booker",              "Pick #13 · 2015 · Escolta · 198 cm",      "Devin Booker NBA highlights"),
    "PG": ("Shai Gilgeous-Alexander",   "Pick #11 · 2018 · Base · 198 cm",         "Shai Gilgeous-Alexander highlights"),
}

# ── Funciones ────────────────────────────────────────────────────────────────

def simular(pts, reb, ast, blk, fg, height, wing):
    score = (pts * 0.22 + reb * 0.14 + ast * 0.10 + blk * 0.18
             + fg * 18 + (height - 170) * 0.05 + (wing - 170) * 0.04)
    if score > 14:
        r1, r2, nd = 0.74, 0.18, 0.08
    elif score > 10:
        r1, r2, nd = 0.38, 0.34, 0.28
    elif score > 7:
        r1, r2, nd = 0.12, 0.38, 0.50
    else:
        r1, r2, nd = 0.04, 0.18, 0.78

    if r1 >= r2 and r1 >= nd:
        ronda, color = "1.ª Ronda", "#16a34a"
        rangos = [("1–10",0.42),("11–20",0.31),("21–30",0.14),("31–40",0.07),("41–50",0.04),("51–60",0.02)]
    elif r2 >= r1 and r2 >= nd:
        ronda, color = "2.ª Ronda", "#d97706"
        rangos = [("1–10",0.02),("11–20",0.06),("21–30",0.10),("31–40",0.26),("41–50",0.32),("51–60",0.24)]
    else:
        ronda, color = "No drafteado", "#94a3b8"
        rangos = [("ND",0.78),("1–10",0.02),("11–20",0.04),("21–30",0.06),("31–40",0.05),("41–50",0.03)]

    top_rango = max(rangos, key=lambda x: x[1])
    conf = max(r1, r2, nd)
    return ronda, color, conf, rangos, top_rango, r1, r2, nd


def norm(val, lo, hi):
    return max(0.0, min(1.0, (val - lo) / (hi - lo)))


def spider_chart(vals, labels):
    n = len(labels)
    angles = [math.pi * 2 * i / n - math.pi / 2 for i in range(n)]
    angles_closed = angles + [angles[0]]
    vals_closed = vals + [vals[0]]
    labels_closed = labels + [labels[0]]

    fig = go.Figure()

    # rejilla
    for ring in [0.25, 0.5, 0.75, 1.0]:
        rx = [math.cos(a) * ring for a in angles_closed]
        ry = [math.sin(a) * ring for a in angles_closed]
        fig.add_trace(go.Scatter(
            x=rx, y=ry, mode="lines",
            line=dict(color="#e2e8f0", width=1),
            showlegend=False, hoverinfo="skip",
        ))
    # radios
    for a in angles:
        fig.add_trace(go.Scatter(
            x=[0, math.cos(a)], y=[0, math.sin(a)], mode="lines",
            line=dict(color="#e2e8f0", width=1),
            showlegend=False, hoverinfo="skip",
        ))

    # área del jugador
    px = [math.cos(a) * v for a, v in zip(angles_closed, vals_closed)]
    py = [math.sin(a) * v for a, v in zip(angles_closed, vals_closed)]
    fig.add_trace(go.Scatter(
        x=px, y=py, mode="lines+markers",
        fill="toself",
        fillcolor="rgba(24,95,165,0.20)",
        line=dict(color="#185FA5", width=2.5),
        marker=dict(color="#185FA5", size=6),
        showlegend=False, hoverinfo="skip",
    ))

    # etiquetas
    for i, (label, a) in enumerate(zip(labels, angles)):
        lx = math.cos(a) * 1.22
        ly = math.sin(a) * 1.22
        fig.add_annotation(
            x=lx, y=ly, text=label,
            showarrow=False,
            font=dict(size=12, color="#475569"),
            xanchor="center", yanchor="middle",
        )

    fig.update_layout(
        xaxis=dict(visible=False, range=[-1.4, 1.4]),
        yaxis=dict(visible=False, range=[-1.4, 1.4], scaleanchor="x"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        height=340,
    )
    return fig


def barras_rango(rangos):
    etiquetas = [r[0] for r in rangos]
    valores   = [r[1] * 100 for r in rangos]
    max_v = max(valores)
    colores = ["#185FA5" if v == max_v else "#e2e8f0" for v in valores]
    txt_col = ["white" if v == max_v else "#64748b" for v in valores]

    fig = go.Figure(go.Bar(
        x=etiquetas, y=valores,
        marker_color=colores,
        marker_line_width=0,
        text=[f"{v:.0f}%" for v in valores],
        textposition="outside",
        textfont=dict(color="#475569", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=200,
        yaxis=dict(visible=False, range=[0, max(valores) * 1.35]),
        xaxis=dict(tickfont=dict(color="#475569", size=11), ticklen=0),
    )
    return fig

# ── Layout ───────────────────────────────────────────────────────────────────

st.markdown("# 🏀 NBA Draft 2026 · Predictor")
st.markdown('<p class="subtitulo">Mueve los sliders e introduce las medidas del jugador. Pulsa Predecir para ver el resultado.</p>', unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1], gap="large")

with col_izq:
    st.markdown("**Estadísticas de temporada**")

    pts  = st.slider("Puntos / partido",      0.0, 40.0, 7.5,  0.5)
    reb  = st.slider("Rebotes / partido",     0.0, 20.0, 4.2,  0.5)
    ast  = st.slider("Asistencias / partido", 0.0, 15.0, 0.5,  0.5)
    blk  = st.slider("Tapones / partido",     0.0,  8.0, 1.4,  0.1)
    fg   = st.slider("% Tiro campo",          0,   100,  52,   1)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("**Medidas físicas (NBA Combine)**")

    height = st.slider("Altura (cm)",      170, 230, 214, 1)
    weight = st.slider("Peso (kg)",         60, 140, 104, 1)
    wing   = st.slider("Envergadura (cm)", 170, 240, 223, 1)
    leap   = st.slider("Salto máximo (cm)", 40, 120,  72, 1)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    pos = st.selectbox("Posición", options=["C","PF","SF","SG","PG"],
                       format_func=lambda x: {
                           "C":"C — Pívot", "PF":"PF — Ala-pívot",
                           "SF":"SF — Alero","SG":"SG — Escolta","PG":"PG — Base"
                       }[x])

    predecir = st.button("Predecir", type="primary", use_container_width=True)

with col_der:
    # spider siempre visible
    spider_labels = ["Puntos","Rebotes","Asist.","Tapones","Tiro %","Altura","Enverg.","Salto"]
    spider_vals = [
        norm(pts,   0,   40),
        norm(reb,   0,   20),
        norm(ast,   0,   15),
        norm(blk,   0,    8),
        norm(fg,    30,  70),
        norm(height,170,230),
        norm(wing,  170,240),
        norm(leap,  40, 120),
    ]
    st.markdown("**Perfil del jugador**")
    st.plotly_chart(spider_chart(spider_vals, spider_labels),
                    use_container_width=True, config={"displayModeBar": False})

    if predecir:
        ronda, color, conf, rangos, top_rango, r1, r2, nd = simular(
            pts, reb, ast, blk, fg / 100, height, wing
        )
        arq  = ARQUETIPOS[pos]
        comp = COMPARABLES[pos]

        st.markdown("**Predicción**")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="resultado-box">
                <div class="res-label">Ronda</div>
                <div class="res-valor" style="color:{color}">{ronda}</div>
                <div class="res-pct">Confianza: {conf*100:.0f}%</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="resultado-box">
                <div class="res-label">Rango picks</div>
                <div class="res-valor">{top_rango[0]}</div>
                <div class="res-pct">Prob: {top_rango[1]*100:.0f}%</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="resultado-box">
                <div class="res-label">Arquetipo</div>
                <div class="res-valor" style="font-size:1rem; padding-top:4px">{arq}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Probabilidad por rango de elección**")
        st.plotly_chart(barras_rango(rangos),
                        use_container_width=True, config={"displayModeBar": False})

        nombre, detalle, ytq = comp
        yt_url = f"https://www.youtube.com/results?search_query={ytq.replace(' ', '+')}"
        st.markdown(f"""
        <div class="comp-box">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
                <div>
                    <div class="comp-nombre">🎬 Comparable histórico: {nombre}</div>
                    <div class="comp-detalle">{detalle}</div>
                </div>
                <a href="{yt_url}" target="_blank" style="
                    display:inline-block; padding:7px 14px;
                    background:#f1f5f9; border:1px solid #e2e8f0;
                    border-radius:8px; font-size:0.82rem; color:#1e293b;
                    text-decoration:none; white-space:nowrap; font-weight:500;">
                    ▶ Ver highlights
                </a>
            </div>
        </div>""", unsafe_allow_html=True)