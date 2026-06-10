import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go

# ── rutas ─────────────────────────────────────────────────────────────────────
BASE        = os.path.dirname(__file__)
PKL_MODELOS = os.path.join(BASE, '..', 'pkl', 'modelos')
PKL_PREPROC = os.path.join(BASE, '..', 'pkl', 'preprocesado')

# ── carga de modelos ──────────────────────────────────────────────────────────
@st.cache_resource
def cargar_modelos():
    rf_draft = joblib.load(os.path.join(PKL_MODELOS, 'rf_draft.pkl'))
    rf_rango = joblib.load(os.path.join(PKL_MODELOS, 'rf_rango.pkl'))
    km       = joblib.load(os.path.join(PKL_MODELOS, 'kmeans_arquetipos.pkl'))
    le_draft = joblib.load(os.path.join(PKL_PREPROC, 'le_target_draft.pkl'))
    le_rango = joblib.load(os.path.join(PKL_PREPROC, 'le_rango.pkl'))
    scaler   = joblib.load(os.path.join(PKL_PREPROC, 'scaler_combine.pkl'))
    return rf_draft, rf_rango, km, le_draft, le_rango, scaler

rf_draft, rf_rango, km, le_draft, le_rango, scaler = cargar_modelos()

# ── columnas exactas de cada modelo ──────────────────────────────────────────
COLS_DRAFT = ['pts','gbpm','bpm','usg','stops','mp','altura_cm','stl','GP','blk',
              'TS_per','stl_per','ogbpm','TO_per','midmade/(midmade+midmiss)',
              'ast/tov','posicion_Wing G','blk_per','posicion_PF/C','treb','ftr',
              'Min_per','AST_per','rimmade/(rimmade+rimmiss)','TP_per','DRB_per',
              'drtg','ast','obpm','eFG','Ortg','dgbpm','ORB_per','dbpm',
              'posicion_Pure PG','twoP_per']

COLS_RANGO = ['gbpm','bpm','posicion_C','usg','pts','posicion_PF/C','stops','drtg',
              'stl','FT_per','dgbpm','ORB_per','ast/tov','rimmade/(rimmade+rimmiss)',
              'twoP_per','Ortg','blk','TO_per','posicion_Wing F','ftr','dbpm',
              'stl_per','eFG','ogbpm','TP_per','Min_per','treb','altura_cm','TS_per',
              'posicion_Pure PG','mp','midmade/(midmade+midmiss)','obpm','blk_per',
              'GP','DRB_per','posicion_Wing G','AST_per']

# ── posiciones reales del dataset ─────────────────────────────────────────────
POSICIONES = ['C','Wing F','Scoring PG','Wing G','Stretch 4','PF/C','Combo G','Pure PG','desconocido']

# ── arquetipos ────────────────────────────────────────────────────────────────
NOMBRES_GRUPOS = {
    0: 'Pívot clásico',
    1: 'Alero / Escolta versátil',
    2: 'Base / Escolta pequeño',
    3: 'Base / Escolta explosivo',
    4: 'Alero atlético explosivo',
    5: 'Pívot élite moderno',
    6: 'Alero / Escolta duro',
}

REFERENTES = {
    'Pívot clásico':            {'jugadores': ['Dwight Howard','DeAndre Jordan','Rudy Gobert',"Shaquille O'Neal"],       'yt': 'https://www.youtube.com/results?search_query=Dwight+Howard+best+highlights'},
    'Alero / Escolta versátil': {'jugadores': ['Kevin Love','Blake Griffin','Draymond Green','Tobias Harris'],           'yt': 'https://www.youtube.com/results?search_query=Blake+Griffin+best+highlights'},
    'Base / Escolta pequeño':   {'jugadores': ['Chris Paul','Isaiah Thomas','Kemba Walker','Trae Young'],                'yt': 'https://www.youtube.com/results?search_query=Trae+Young+best+highlights'},
    'Base / Escolta explosivo': {'jugadores': ['Ja Morant',"De'Aaron Fox",'Russell Westbrook','Derrick Rose'],           'yt': 'https://www.youtube.com/results?search_query=Ja+Morant+best+highlights'},
    'Alero atlético explosivo': {'jugadores': ['Giannis Antetokounmpo','LeBron James','Zion Williamson','Jaylen Brown'], 'yt': 'https://www.youtube.com/results?search_query=Giannis+Antetokounmpo+best+highlights'},
    'Pívot élite moderno':      {'jugadores': ['Anthony Davis','Joel Embiid','Nikola Jokic','Karl-Anthony Towns'],       'yt': 'https://www.youtube.com/results?search_query=Anthony+Davis+best+highlights'},
    'Alero / Escolta duro':     {'jugadores': ['Carmelo Anthony','Rudy Gay','DeMar DeRozan','Paul Pierce'],              'yt': 'https://www.youtube.com/results?search_query=DeMar+DeRozan+best+highlights'},
}

# ── stats de los tres españoles ───────────────────────────────────────────────
# todos los campos que pueden aparecer en COLS_DRAFT o COLS_RANGO
def stats_aday():
    return {
        'pts':12.1,'gbpm':4.8,'bpm':5.2,'usg':22.5,'stops':0.12,'mp':23.4,
        'altura_cm':221.0,'stl':0.5,'GP':40,'blk':2.6,'TS_per':60.0,
        'stl_per':1.8,'ogbpm':2.5,'TO_per':12.5,
        'midmade/(midmade+midmiss)':0.48,'ast/tov':1.9,
        'blk_per':8.5,'treb':6.8,'ftr':0.28,'Min_per':23.4,'AST_per':12.0,
        'rimmade/(rimmade+rimmiss)':0.72,'TP_per':30.0,'DRB_per':18.2,
        'drtg':98.0,'ast':2.4,'obpm':2.8,'eFG':67.3,'Ortg':118.0,
        'dgbpm':2.3,'ORB_per':10.5,'dbpm':2.4,'twoP_per':66.8,'FT_per':56.4,
    }

def stats_baba():
    return {
        'pts':13.0,'gbpm':4.2,'bpm':4.8,'usg':24.0,'stops':0.14,'mp':31.8,
        'altura_cm':211.0,'stl':0.8,'GP':31,'blk':1.2,'TS_per':58.0,
        'stl_per':2.1,'ogbpm':2.0,'TO_per':14.0,
        'midmade/(midmade+midmiss)':0.44,'ast/tov':2.6,
        'blk_per':4.2,'treb':10.3,'ftr':0.34,'Min_per':31.8,'AST_per':16.5,
        'rimmade/(rimmade+rimmiss)':0.65,'TP_per':19.2,'DRB_per':24.5,
        'drtg':99.0,'ast':3.7,'obpm':2.2,'eFG':54.6,'Ortg':112.0,
        'dgbpm':2.2,'ORB_per':12.0,'dbpm':2.6,'twoP_per':52.9,'FT_per':65.8,
    }

def stats_sergio():
    return {
        'pts':9.6,'gbpm':2.2,'bpm':2.5,'usg':20.0,'stops':0.10,'mp':19.5,
        'altura_cm':196.0,'stl':0.8,'GP':34,'blk':0.3,'TS_per':55.0,
        'stl_per':2.8,'ogbpm':1.0,'TO_per':13.0,
        'midmade/(midmade+midmiss)':0.42,'ast/tov':2.8,
        'blk_per':1.0,'treb':3.0,'ftr':0.22,'Min_per':19.5,'AST_per':22.0,
        'rimmade/(rimmade+rimmiss)':0.55,'TP_per':40.7,'DRB_per':9.0,
        'drtg':102.0,'ast':3.7,'obpm':1.2,'eFG':48.0,'Ortg':108.0,
        'dgbpm':1.2,'ORB_per':2.5,'dbpm':1.3,'twoP_per':44.0,'FT_per':78.0,
    }

ESPANOLES = {
    'Aday Mara': {
        'equipo':'Michigan Wolverines (NCAA)','posicion':'C',
        'temporada':'2025-26','nota':None,'altura_cm':221,
        'display':{'pts':12.1,'treb':6.8,'ast':2.4,'blk':2.6,'stl':0.5,'fg_pct':66.8},
        'modelo': stats_aday(),
        'combine':{'HEIGHT_W_SHOES':87.25,'WEIGHT':240.0,'WINGSPAN':96.0,
                   'STANDING_REACH':113.0,'MAX_VERTICAL_LEAP':24.0,
                   'LANE_AGILITY_TIME':11.8,'THREE_QUARTER_SPRINT':3.5},
    },
    'Baba Miller': {
        'equipo':'Cincinnati Bearcats (NCAA)','posicion':'Wing F',
        'temporada':'2025-26','nota':None,'altura_cm':211,
        'display':{'pts':13.0,'treb':10.3,'ast':3.7,'blk':1.2,'stl':0.8,'fg_pct':52.9},
        'modelo': stats_baba(),
        'combine':{'HEIGHT_W_SHOES':83.5,'WEIGHT':208.2,'WINGSPAN':85.75,
                   'STANDING_REACH':111.0,'MAX_VERTICAL_LEAP':34.5,
                   'LANE_AGILITY_TIME':11.2,'THREE_QUARTER_SPRINT':3.3},
    },
    'Sergio de Larrea': {
        'equipo':'Valencia Basket (ACB / EuroLeague)','posicion':'Scoring PG',
        'temporada':'2025-26',
        'nota':'⚠️ Stats de ACB/EuroLeague. El modelo fue entrenado con datos NCAA — predicción orientativa.',
        'altura_cm':196,
        'display':{'pts':9.6,'treb':3.0,'ast':3.7,'blk':0.3,'stl':0.8,'fg_pct':44.0},
        'modelo': stats_sergio(),
        'combine':{'HEIGHT_W_SHOES':77.5,'WEIGHT':175.0,'WINGSPAN':80.0,
                   'STANDING_REACH':100.0,'MAX_VERTICAL_LEAP':30.0,
                   'LANE_AGILITY_TIME':10.8,'THREE_QUARTER_SPRINT':3.15},
    },
}

# ── funciones ─────────────────────────────────────────────────────────────────
def preparar_features(modelo_dict, posicion, cols_modelo):
    fila = dict(modelo_dict)
    for p in POSICIONES:
        fila[f'posicion_{p}'] = 1 if posicion == p else 0
    df = pd.DataFrame([fila])
    for col in cols_modelo:
        if col not in df.columns:
            df[col] = 0.0
    return df[cols_modelo]


def predecir_arquetipo(combine_data):
    vector = pd.DataFrame([combine_data])
    cluster_id = km.predict(scaler.transform(vector))[0]
    arquetipo  = NOMBRES_GRUPOS[cluster_id]
    info       = REFERENTES.get(arquetipo, {'jugadores':[],'yt':''})
    return arquetipo, info['jugadores'], info['yt']


def spider_chart(d, nombre):
    cats   = ['Puntos','Rebotes','Asistencias','Tapones','Robos','FG%']
    maxs   = [25.0, 15.0, 10.0, 4.0, 3.0, 70.0]
    vals   = [min(10, round(d[k]/m*10,1)) for k,m in
              zip(['pts','treb','ast','blk','stl','fg_pct'], maxs)]
    v2 = vals + [vals[0]]
    c2 = cats  + [cats[0]]
    fig = go.Figure(go.Scatterpolar(
        r=v2, theta=c2, fill='toself',
        fillcolor='rgba(249,115,22,0.2)',
        line=dict(color='#f97316', width=2),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='#0d1117',
            radialaxis=dict(visible=True, range=[0,10], color='#555', gridcolor='#333'),
            angularaxis=dict(color='white', gridcolor='#333'),
        ),
        paper_bgcolor='#0d1117', font=dict(color='white', size=12),
        showlegend=False, height=300,
        margin=dict(l=40,r=40,t=30,b=30),
    )
    return fig


def barras_h(clases, probas, titulo):
    cols = ['#f97316' if p == max(probas) else '#1e3a5f' for p in probas]
    fig  = go.Figure(go.Bar(
        x=probas, y=clases, orientation='h',
        marker_color=cols,
        text=[f'{p:.1%}' for p in probas],
        textposition='outside',
    ))
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=13)),
        xaxis=dict(range=[0,1], tickformat='.0%', color='#aaa'),
        yaxis=dict(color='white'),
        paper_bgcolor='#0d1117', plot_bgcolor='#0d1117',
        font=dict(color='white'), height=250,
        margin=dict(l=10,r=70,t=40,b=10),
    )
    return fig


def mostrar_jugador(nombre, datos):
    st.markdown(f"### {nombre}")
    st.caption(f"{datos['equipo']} · {datos['temporada']} · {datos['posicion']} · {datos['altura_cm']} cm")
    if datos['nota']:
        st.warning(datos['nota'])

    # stats y spider siempre visibles
    col_s, col_p, col_a = st.columns([1, 1.6, 1])

    with col_s:
        st.plotly_chart(spider_chart(datos['display'], nombre), use_container_width=True)
        d = datos['display']
        r1, r2 = st.columns(3), st.columns(3)
        r1[0].metric("PTS", d['pts'])
        r1[1].metric("REB", d['treb'])
        r1[2].metric("AST", d['ast'])
        r2[0].metric("BLK", d['blk'])
        r2[1].metric("STL", d['stl'])
        r2[2].metric("FG%", f"{d['fg_pct']}%")

    with col_p:
        if st.button(f'🔮 Predecir draft de {nombre}', key=f'btn_{nombre}', use_container_width=True):
            st.session_state[f'pred_{nombre}'] = True

        if st.session_state.get(f'pred_{nombre}'):
            X_d    = preparar_features(datos['modelo'], datos['posicion'], COLS_DRAFT)
            pd_    = rf_draft.predict_proba(X_d)[0]
            pred_d = le_draft.inverse_transform(rf_draft.predict(X_d))[0]

            X_r    = preparar_features(datos['modelo'], datos['posicion'], COLS_RANGO)
            pr_    = rf_rango.predict_proba(X_r)[0]
            pred_r = le_rango.inverse_transform(rf_rango.predict(X_r))[0]

            st.plotly_chart(barras_h(le_draft.classes_, pd_, f'Ronda predicha: {pred_d}'), use_container_width=True)
            st.plotly_chart(barras_h(le_rango.classes_, pr_, f'Rango pick predicho: {pred_r}'), use_container_width=True)

    with col_a:
        if st.session_state.get(f'pred_{nombre}'):
            arq, refs, yt = predecir_arquetipo(datos['combine'])
            st.markdown('**Arquetipo físico**')
            st.markdown(f'### {arq}')
            st.markdown('**Referentes NBA:**')
            for r in refs:
                st.markdown(f'• {r}')
            st.markdown(f'[▶ Ver highlights en YouTube]({yt})')

    st.divider()


# ── UI ────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title='NBA Draft 2026', page_icon='🏀', layout='wide')

st.markdown("""
<style>
.stApp{background-color:#0d1117;color:white}
h1,h2,h3{color:white}
[data-testid="stMetricValue"]{color:white;font-size:1.2rem;font-weight:bold}
[data-testid="stMetricLabel"]{color:#888;font-size:0.72rem}
.stTabs [data-baseweb="tab"]{color:#aaa}
.stTabs [aria-selected="true"]{color:#f97316;border-bottom:2px solid #f97316}
</style>
""", unsafe_allow_html=True)

st.title('🏀 NBA Draft 2026 — Predicción de españoles')
st.markdown('Modelos Random Forest entrenados con datos NCAA 2009-2026.')

tab1, tab2 = st.tabs(['🇪🇸 Prospects españoles', '🎮 Modo libre'])

with tab1:
    st.markdown('## Predicciones 2026 Draft')
    for nombre, datos in ESPANOLES.items():
        mostrar_jugador(nombre, datos)

with tab2:
    st.markdown('## ¿Entrarías en el draft?')
    st.markdown('Introduce tus stats y medidas físicas.')

    with st.form('form'):
        c1,c2,c3 = st.columns(3)
        pts  = c1.number_input('Puntos',      0.0, 50.0, 10.0, 0.1)
        treb = c2.number_input('Rebotes',     0.0, 25.0, 5.0,  0.1)
        ast  = c3.number_input('Asistencias', 0.0, 20.0, 3.0,  0.1)

        c4,c5,c6 = st.columns(3)
        stl  = c4.number_input('Robos',   0.0, 10.0, 1.0,  0.1)
        blk  = c5.number_input('Tapones', 0.0, 10.0, 0.5,  0.1)
        fg   = c6.number_input('FG%',     0.0, 100.0,45.0, 0.1)

        c7,c8,c9 = st.columns(3)
        ft   = c7.number_input('FT%',         0.0, 100.0, 70.0, 0.1)
        mins = c8.number_input('Min/partido', 0.0, 40.0,  25.0, 0.1)
        gp   = c9.number_input('Partidos',    1,   40,    30,   1)

        c10,c11 = st.columns(2)
        pos    = c10.selectbox('Posición', POSICIONES)
        altura = c11.number_input('Altura (cm)', 150, 240, 190)

        st.markdown('### Medidas físicas')
        m1,m2,m3 = st.columns(3)
        peso    = m1.number_input('Peso (kg)',           50,  160, 85)
        enverg  = m2.number_input('Envergadura (cm)',    150, 260, 195)
        alcance = m3.number_input('Alcance en pie (cm)', 200, 320, 250)

        m4,m5,m6 = st.columns(3)
        salto    = m4.number_input('Salto máximo (cm)',      30,  120, 60)
        agilidad = m5.number_input('Tiempo agilidad (seg)',  9.0, 14.0,11.0,0.1)
        sprint   = m6.number_input('Sprint 3/4 pista (seg)', 2.5, 5.0, 3.4, 0.1)

        ok = st.form_submit_button('🔮 Predecir', use_container_width=True)

    if ok:
        bpm_e  = (pts-10)*0.15 + (treb-5)*0.1 + (ast-3)*0.12 - 2.0
        usg_e  = min(35, max(12, pts/max(mins,1)*100*0.3))
        efg_e  = fg * 0.95

        m = {
            'pts':pts,'treb':treb,'ast':ast,'stl':stl,'blk':blk,
            'mp':mins,'Min_per':mins,'GP':gp,'altura_cm':float(altura),
            'eFG':efg_e,'TS_per':fg*0.92,'FT_per':ft,'ftr':ft/300,
            'twoP_per':fg*0.85,'TP_per':fg*0.33,
            'ORB_per':treb*0.35*5,'DRB_per':treb*0.65*5,
            'AST_per':ast/max(mins,1)*80,'TO_per':ast*0.3*3,
            'stl_per':stl/max(mins,1)*80,'blk_per':blk/max(mins,1)*80,
            'usg':usg_e,'Ortg':100+(efg_e-48)*0.4,'drtg':100.0,
            'bpm':bpm_e,'obpm':bpm_e*0.55,'dbpm':bpm_e*0.45,
            'gbpm':bpm_e*0.9,'ogbpm':bpm_e*0.5,'dgbpm':bpm_e*0.4,
            'stops':stl*0.04+blk*0.03,
            'ast/tov':ast/max(ast*0.25+0.5,0.5),
            'rimmade/(rimmade+rimmiss)':min(0.85,fg/100*1.2),
            'midmade/(midmade+midmiss)':min(0.65,fg/100*0.9),
        }
        display = {'pts':pts,'treb':treb,'ast':ast,'blk':blk,'stl':stl,'fg_pct':fg}
        combine = {
            'HEIGHT_W_SHOES':altura/2.54,'WEIGHT':peso*2.205,
            'WINGSPAN':enverg/2.54,'STANDING_REACH':alcance/2.54,
            'MAX_VERTICAL_LEAP':salto/2.54,
            'LANE_AGILITY_TIME':agilidad,'THREE_QUARTER_SPRINT':sprint,
        }

        X_d = preparar_features(m, pos, COLS_DRAFT)
        pd_  = rf_draft.predict_proba(X_d)[0]
        pred_d = le_draft.inverse_transform(rf_draft.predict(X_d))[0]

        X_r = preparar_features(m, pos, COLS_RANGO)
        pr_  = rf_rango.predict_proba(X_r)[0]
        pred_r = le_rango.inverse_transform(rf_rango.predict(X_r))[0]

        arq, refs, yt = predecir_arquetipo(combine)

        st.markdown('---')
        st.markdown('## 📊 Resultado')
        cs, cp, ca = st.columns([1,1.6,1])
        with cs:
            st.plotly_chart(spider_chart(display,'Tú'), use_container_width=True)
        with cp:
            st.plotly_chart(barras_h(le_draft.classes_, pd_, f'Ronda predicha: {pred_d}'), use_container_width=True)
            st.plotly_chart(barras_h(le_rango.classes_, pr_, f'Rango pick predicho: {pred_r}'), use_container_width=True)
        with ca:
            st.markdown('**Arquetipo físico**')
            st.markdown(f'### {arq}')
            for r in refs:
                st.markdown(f'• {r}')
            st.markdown(f'[▶ Ver highlights en YouTube]({yt})')
        st.caption('⚠️ Métricas avanzadas estimadas — resultados orientativos.')