# funciones.py
# módulo central del proyecto nba draft 2026
# contiene toda la lógica de carga, entrenamiento, clustering y predicción

import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from scipy.spatial.distance import cdist
from xgboost import XGBClassifier


# ── rutas ────────────────────────────────────────────────────────────────────

RUTA_DATOS   = '../datos'
RUTA_MODELOS = '../modelos'


# ══════════════════════════════════════════════════════════════════════════════
# bloque 1 — carga y preparación de datos
# ══════════════════════════════════════════════════════════════════════════════

def cargar_ncaa():
    """carga el dataset de stats universitarias y europeas con las targets ya creadas."""
    ruta = os.path.join(RUTA_DATOS, 'ncaa.csv')
    ncaa = pd.read_csv(ruta)
    print(f"ncaa cargado: {ncaa.shape}")
    return ncaa


def cargar_combine_draft():
    """carga y mergea combine físico + carrera nba. devuelve solo filas completas."""
    combine = pd.read_csv(os.path.join(RUTA_DATOS, 'combine_final.csv'))
    draft   = pd.read_csv(os.path.join(RUTA_DATOS, 'nbaplayersdraft.csv'))

    # normalizo nombres para el merge
    combine['nombre_norm'] = combine['PLAYER_NAME'].str.lower().str.strip()
    draft['nombre_norm']   = draft['player'].str.lower().str.strip()

    df = pd.merge(combine, draft, on='nombre_norm', how='inner')
    print(f"combine + draft mergeados: {df.shape}")
    return df


# ══════════════════════════════════════════════════════════════════════════════
# bloque 2 — modelo de ronda (nd / r1 / r2)
# ══════════════════════════════════════════════════════════════════════════════

def preparar_features_ronda(ncaa):
    """encodea posicion y devuelve X, y y los encoders."""
    le_posicion = LabelEncoder()
    ncaa = ncaa.copy()
    ncaa['posicion_enc'] = le_posicion.fit_transform(ncaa['posicion'])

    features = [c for c in ncaa.columns if c not in ['posicion', 'ronda', 'rango_pick']]

    le_ronda = LabelEncoder()
    X = ncaa[features]
    y = le_ronda.fit_transform(ncaa['ronda'])

    return X, y, features, le_posicion, le_ronda


def entrenar_modelo_ronda(X, y):
    """entrena xgboost para predecir ronda con pesos para compensar el desbalance."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=11, stratify=y
    )

    # calculo pesos por clase: las minoritarias pesan más
    conteos       = np.bincount(y_train)
    pesos_clase   = len(y_train) / (len(conteos) * conteos)
    pesos_muestra = np.array([pesos_clase[c] for c in y_train])

    modelo = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='mlogloss',
        random_state=11,
        n_jobs=-1
    )

    modelo.fit(X_train, y_train, sample_weight=pesos_muestra)

    # evalúo en test y muestro el report
    y_pred = modelo.predict(X_test)
    print("\n=== modelo ronda — classification report ===")
    print(classification_report(y_test, y_pred))

    return modelo


# ══════════════════════════════════════════════════════════════════════════════
# bloque 3 — modelo de rango de pick
# ══════════════════════════════════════════════════════════════════════════════

def preparar_features_pick(ncaa, features):
    """filtra solo drafteados y encodea el rango de pick."""
    drafteados = ncaa[ncaa['rango_pick'] != 'ND'].copy()

    le_pick = LabelEncoder()
    X = drafteados[features]
    y = le_pick.fit_transform(drafteados['rango_pick'])

    print(f"jugadores drafteados para modelo pick: {len(drafteados)}")
    return X, y, le_pick


def entrenar_modelo_pick(X, y):
    """entrena xgboost para predecir el rango de pick entre los drafteados."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=11, stratify=y
    )

    modelo = XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='mlogloss',
        random_state=11,
        n_jobs=-1
    )

    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    print("\n=== modelo pick — classification report ===")
    print(classification_report(y_test, y_pred))

    return modelo


# ══════════════════════════════════════════════════════════════════════════════
# bloque 4 — clustering de arquetipos físicos
# ══════════════════════════════════════════════════════════════════════════════

# columnas físicas del combine que usa el clustering
FISICAS = [
    'HEIGHT_W_SHOES', 'WEIGHT', 'WINGSPAN', 'STANDING_REACH',
    'BODY_FAT_PCT', 'HAND_LENGTH', 'HAND_WIDTH',
    'STANDING_VERTICAL_LEAP', 'MAX_VERTICAL_LEAP',
    'LANE_AGILITY_TIME', 'THREE_QUARTER_SPRINT', 'BENCH_PRESS'
]

# nombres de los clusters — ajustar tras ver el heatmap de perfiles
NOMBRES_CLUSTER = {
    0: 'Ala versátil',
    1: 'Escolta/Alero atlético',
    2: 'Pivot de poder',
    3: 'Ala-Pivot móvil',
    4: 'Base explosivo',
    5: 'Base/Escolta físico',
    6: 'Interior atlético',
}


def entrenar_clustering(df):
    """escala las físicas y entrena kmeans con k=7. devuelve modelo, scaler y df con clusters."""
    X = df[FISICAS].copy()

    escalado = StandardScaler()
    X_escalado = escalado.fit_transform(X)

    km = KMeans(n_clusters=7, random_state=11, n_init=10)
    df = df.copy()
    df['cluster']   = km.fit_predict(X_escalado)
    df['arquetipo'] = df['cluster'].map(NOMBRES_CLUSTER)

    print(f"\ndistribución de arquetipos:")
    print(df['arquetipo'].value_counts())

    return km, escalado, df


# ══════════════════════════════════════════════════════════════════════════════
# bloque 5 — exportación e importación de modelos
# ══════════════════════════════════════════════════════════════════════════════

def exportar_modelos(modelo_ronda, modelo_pick, km, escalado,
                     le_posicion, le_ronda, le_pick, features, df_arquetipos):
    """guarda todos los modelos y encoders en la carpeta modelos/."""
    os.makedirs(RUTA_MODELOS, exist_ok=True)

    joblib.dump(modelo_ronda,    os.path.join(RUTA_MODELOS, 'modelo_ronda.pkl'))
    joblib.dump(modelo_pick,     os.path.join(RUTA_MODELOS, 'modelo_pick.pkl'))
    joblib.dump(km,              os.path.join(RUTA_MODELOS, 'km_arquetipos.pkl'))
    joblib.dump(escalado,        os.path.join(RUTA_MODELOS, 'escalado_arquetipos.pkl'))
    joblib.dump(le_posicion,     os.path.join(RUTA_MODELOS, 'le_posicion.pkl'))
    joblib.dump(le_ronda,        os.path.join(RUTA_MODELOS, 'le_ronda.pkl'))
    joblib.dump(le_pick,         os.path.join(RUTA_MODELOS, 'le_pick.pkl'))
    joblib.dump(features,        os.path.join(RUTA_MODELOS, 'features.pkl'))
    joblib.dump(NOMBRES_CLUSTER, os.path.join(RUTA_MODELOS, 'nombres_cluster.pkl'))

    df_arquetipos.to_csv(os.path.join(RUTA_MODELOS, 'df_arquetipos.csv'), index=False)

    print(f"\nmodelos exportados en '{RUTA_MODELOS}/'")


def cargar_modelos():
    """carga todos los modelos y encoders desde disco. devuelve un dict con todo."""
    m = {}
    m['modelo_ronda']    = joblib.load(os.path.join(RUTA_MODELOS, 'modelo_ronda.pkl'))
    m['modelo_pick']     = joblib.load(os.path.join(RUTA_MODELOS, 'modelo_pick.pkl'))
    m['km']              = joblib.load(os.path.join(RUTA_MODELOS, 'km_arquetipos.pkl'))
    m['escalado']        = joblib.load(os.path.join(RUTA_MODELOS, 'escalado_arquetipos.pkl'))
    m['le_posicion']     = joblib.load(os.path.join(RUTA_MODELOS, 'le_posicion.pkl'))
    m['le_ronda']        = joblib.load(os.path.join(RUTA_MODELOS, 'le_ronda.pkl'))
    m['le_pick']         = joblib.load(os.path.join(RUTA_MODELOS, 'le_pick.pkl'))
    m['features']        = joblib.load(os.path.join(RUTA_MODELOS, 'features.pkl'))
    m['nombres_cluster'] = joblib.load(os.path.join(RUTA_MODELOS, 'nombres_cluster.pkl'))
    m['df_arquetipos']   = pd.read_csv(os.path.join(RUTA_MODELOS, 'df_arquetipos.csv'))
    print("modelos cargados ✓")
    return m


# ══════════════════════════════════════════════════════════════════════════════
# bloque 6 — predicciones
# ══════════════════════════════════════════════════════════════════════════════

def predecir_draft(stats_jugador, m):
    """
    recibe un dict con las stats de juego del jugador y devuelve:
    - ronda predicha (nd / r1 / r2)
    - probabilidades de cada clase
    - rango de pick (solo si no es nd)
    """
    # encodeo la posición con el encoder entrenado
    posicion_enc = m['le_posicion'].transform([stats_jugador['posicion']])[0]
    stats_jugador = {**stats_jugador, 'posicion_enc': posicion_enc}

    # construyo el dataframe en el orden exacto de features
    X = pd.DataFrame([stats_jugador])[m['features']]

    # modelo 1: ronda
    pred_ronda_enc = m['modelo_ronda'].predict(X)[0]
    pred_ronda     = m['le_ronda'].inverse_transform([pred_ronda_enc])[0]
    proba_ronda    = m['modelo_ronda'].predict_proba(X)[0]

    resultado = {
        'ronda'       : pred_ronda,
        'proba_ronda' : dict(zip(m['le_ronda'].classes_, proba_ronda.round(3))),
        'rango_pick'  : None,
        'proba_pick'  : None,
    }

    # modelo 2: rango de pick (solo si no es nd)
    if pred_ronda != 'ND':
        pred_pick_enc = m['modelo_pick'].predict(X)[0]
        pred_pick     = m['le_pick'].inverse_transform([pred_pick_enc])[0]
        proba_pick    = m['modelo_pick'].predict_proba(X)[0]
        resultado['rango_pick'] = pred_pick
        resultado['proba_pick'] = dict(zip(m['le_pick'].classes_, proba_pick.round(3)))

    return resultado


def predecir_arquetipo(fisicas_metrico, m, top_n=3):
    """
    recibe un dict con físicas en unidades métricas (cm / kg),
    asigna el arquetipo y devuelve los top_n comparables históricos y actuales.
    """
    # conversión a pulgadas y libras (unidades del modelo)
    cm_a_pulg = 1 / 2.54
    kg_a_lb   = 2.20462

    fisicas_imperial = {
        'HEIGHT_W_SHOES'        : fisicas_metrico['altura_cm']     * cm_a_pulg,
        'WEIGHT'                : fisicas_metrico['peso_kg']        * kg_a_lb,
        'WINGSPAN'              : fisicas_metrico['envergadura_cm'] * cm_a_pulg,
        'STANDING_REACH'        : fisicas_metrico['alcance_cm']     * cm_a_pulg,
        'BODY_FAT_PCT'          : fisicas_metrico['grasa_pct'],
        'HAND_LENGTH'           : fisicas_metrico['mano_largo_cm']  * cm_a_pulg,
        'HAND_WIDTH'            : fisicas_metrico['mano_ancho_cm']  * cm_a_pulg,
        'STANDING_VERTICAL_LEAP': fisicas_metrico['salto_est_cm']  * cm_a_pulg,
        'MAX_VERTICAL_LEAP'     : fisicas_metrico['salto_max_cm']  * cm_a_pulg,
        'LANE_AGILITY_TIME'     : fisicas_metrico['agilidad_seg'],
        'THREE_QUARTER_SPRINT'  : fisicas_metrico['sprint_seg'],
        'BENCH_PRESS'           : fisicas_metrico['banca_reps'],
    }

    fila      = pd.DataFrame([fisicas_imperial])[FISICAS]
    fila_esc  = m['escalado'].transform(fila)

    # arquetipo asignado por el kmeans
    cluster   = m['km'].predict(fila_esc)[0]
    arquetipo = m['nombres_cluster'][cluster]

    # distancias a todos los jugadores del dataset
    df        = m['df_arquetipos']
    X_ref_esc = m['escalado'].transform(df[FISICAS])
    distancias = cdist(fila_esc, X_ref_esc, metric='euclidean')[0]

    dist_max  = distancias.max()
    scores    = (1 - distancias / dist_max) * 100

    df = df.copy()
    df['similitud'] = scores.round(1)
    df['distancia'] = distancias

    cols = ['player', 'year', 'overall_pick', 'POSITION',
            'points_per_game', 'average_total_rebounds',
            'average_assists', 'box_plus_minus', 'similitud']

    historicos = (df[df['year'] <= 2014]
                  .sort_values('distancia')
                  .head(top_n)[cols]
                  .reset_index(drop=True))

    activos    = (df[df['year'] >= 2015]
                  .sort_values('distancia')
                  .head(top_n)[cols]
                  .reset_index(drop=True))

    return arquetipo, historicos, activos


# ══════════════════════════════════════════════════════════════════════════════
# bloque 7 — utilidades de consola
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_resultado_draft(nombre, resultado):
    """imprime el resultado de predicción de draft de forma legible."""
    sep = '=' * 50
    print(f"\n{sep}")
    print(f"  {nombre.upper()}")
    print(sep)

    print(f"\n→ ronda predicha: {resultado['ronda']}")
    for clase, prob in resultado['proba_ronda'].items():
        print(f"   {clase}: {prob:.1%}")

    if resultado['rango_pick']:
        print(f"\n→ rango de pick predicho: {resultado['rango_pick']}")
        for clase, prob in resultado['proba_pick'].items():
            print(f"   {clase}: {prob:.1%}")
    else:
        print("\n→ el modelo lo clasifica como no drafteado")


def mostrar_resultado_arquetipo(nombre, arquetipo, historicos, activos):
    """imprime el arquetipo y los comparables de forma legible."""
    print(f"\n→ arquetipo físico: {arquetipo}")

    print(f"\n── top 3 comparables históricos (draft ≤ 2014) ──")
    print(historicos.to_string(index=False))

    print(f"\n── top 3 comparables activos (draft ≥ 2015) ──")
    print(activos.to_string(index=False))


def pedir_stats_juego(posiciones_validas):
    """solicita al usuario las stats de juego por consola. devuelve un dict."""
    print("\n── stats de juego ──────────────────────────────")
    print(f"posiciones válidas: {', '.join(posiciones_validas)}\n")

    stats = {}
    stats['posicion']  = input("posición: ").strip()
    stats['GP']        = float(input("partidos jugados (GP): "))
    stats['Min_per']   = float(input("minutos por partido: "))
    stats['pts']       = float(input("puntos por partido: "))
    stats['treb']      = float(input("rebotes por partido: "))
    stats['ast']       = float(input("asistencias por partido: "))
    stats['blk']       = float(input("tapones por partido: "))
    stats['stl']       = float(input("robos por partido: "))
    stats['bpm']       = float(input("box plus/minus (bpm): "))
    stats['TS_per']    = float(input("true shooting % (ej: 0.58): "))
    stats['usg']       = float(input("usage rate (ej: 22.5): "))
    stats['altura_cm'] = float(input("altura en cm: "))

    return stats


def pedir_fisicas():
    """solicita al usuario las medidas físicas del combine por consola. devuelve un dict."""
    print("\n── medidas físicas del combine ─────────────────")

    fisicas = {}
    fisicas['altura_cm']      = float(input("altura con zapatillas (cm): "))
    fisicas['peso_kg']        = float(input("peso (kg): "))
    fisicas['envergadura_cm'] = float(input("envergadura (cm): "))
    fisicas['alcance_cm']     = float(input("alcance estático (cm): "))
    fisicas['grasa_pct']      = float(input("% grasa corporal: "))
    fisicas['mano_largo_cm']  = float(input("longitud de mano (cm): "))
    fisicas['mano_ancho_cm']  = float(input("anchura de mano (cm): "))
    fisicas['salto_est_cm']   = float(input("salto vertical estático (cm): "))
    fisicas['salto_max_cm']   = float(input("salto vertical con carrerilla (cm): "))
    fisicas['agilidad_seg']   = float(input("lane agility (seg): "))
    fisicas['sprint_seg']     = float(input("sprint 3/4 pista (seg): "))
    fisicas['banca_reps']     = int(input("repeticiones banca 185 lbs: "))

    return fisicas
