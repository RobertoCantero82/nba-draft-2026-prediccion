# modelos.py
# aqui cargo los modelos entrenados y hago las predicciones

import joblib
import pandas as pd

from config import CARPETA_PKL, ESTADISTICAS


def cargar_modelos():
    # cargo el modelo de ronda (Random Forest sin posicion) y su codificador
    modelo_ronda = joblib.load(CARPETA_PKL / "modelos" / "modelo_ronda_sin_posicion.pkl")
    le_ronda = joblib.load(CARPETA_PKL / "preprocesado" / "le_ronda_sin_posicion.pkl")
    # cargo el modelo de rango de pick (XGBoost sin posicion) y su codificador
    modelo_rango = joblib.load(CARPETA_PKL / "modelos" / "modelo_rango_sin_posicion.pkl")
    le_rango = joblib.load(CARPETA_PKL / "preprocesado" / "le_rango_sin_posicion.pkl")
    # devuelvo los cuatro objetos juntos
    return modelo_ronda, le_ronda, modelo_rango, le_rango


def predecir(jugador, modelo, codificador):
    # creo un dataframe con todas las variables del modelo puestas a 0
    variables_modelo = modelo.feature_names_in_
    X = pd.DataFrame(0, index=[0], columns=variables_modelo)
    # relleno solo las estadisticas que tengo del jugador
    for estadistica in ESTADISTICAS:
        if estadistica in X.columns:
            X[estadistica] = jugador[estadistica]
    # calculo la probabilidad de cada clase
    probabilidades = modelo.predict_proba(X)[0]
    # asocio cada clase con su probabilidad y lo devuelvo como diccionario
    clases = codificador.classes_
    return dict(zip(clases, probabilidades))


def prob_draft(probs_ronda):
    # sumo todo lo que no sea ND para sacar la probabilidad de ser drafteado (en %)
    return sum(p for clase, p in probs_ronda.items() if clase != "ND") * 100
