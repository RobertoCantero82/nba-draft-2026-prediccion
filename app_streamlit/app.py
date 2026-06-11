import streamlit as st
import pandas as pd
import joblib

# Cargamos el modelo y la estructura de columnas exacta
modelo = joblib.load('modelo_v2_XGBC.joblib')
columnas_entrenamiento = joblib.load('columnas_modelo.joblib')

# Carga también tus datos procesados para usar las medias (como vimos antes)
ncaa_final = pd.read_csv('ncaa_final.csv') 
X_base = ncaa_final.drop(columns=['ronda', 'rango_pick'])
X_base = pd.get_dummies(X_base, columns=['posicion'], drop_first=False)
medias_jugadores = X_base.mean()

# ... Aquí van tus inputs de Streamlit (pts, treb, ast, posicion_seleccionada) ...

if st.button("🔮 Predecir posición en el Draft"):
    # Creamos el DataFrame usando el listado de columnas exacto del entrenamiento
    X_manual = pd.DataFrame(0, index=[0], columns=columnas_entrenamiento)
    
    # Rellenamos con las medias para que no tenga ceros conflictivos
    for col in columnas_entrenamiento:
        if col in medias_jugadores:
            X_manual[col] = medias_jugadores[col]
            
    # Sobrescribimos los inputs que ha introducido el usuario en la interfaz
    X_manual['pts'] = pts
    X_manual['treb'] = treb
    X_manual['ast'] = ast
    
    # Manejo del One-Hot Encoding de la posición seleccionada en la UI
    # Ejemplo: si el usuario elige "Pure PG", ponemos esa columna a 1 y las demás "posicion_..." a 0
    for col in columnas_entrenamiento:
        if col.startswith('posicion_'):
            X_manual[col] = 1 if col == f"posicion_{posicion_seleccionada}" else 0

    # ASEGURAMOS EL ORDEN EXACTO (Esto es lo que soluciona tu ValueError)
    X_manual = X_manual[columnas_entrenamiento]
    
    # Ahora el modelo recibirá exactamente lo que espera
    probs = modelo.predict_proba(X_manual)[0]
    
    # Muestra los resultados en la app...