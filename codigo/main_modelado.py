# main_modelado.py
# entrena los tres modelos (ronda, pick, arquetipos) y los exporta a modelos/
# ejecutar desde la carpeta codigo/: python main_modelado.py

import funciones as fn

# 1 — cargo los datos
ncaa         = fn.cargar_ncaa()
df_arquetipos = fn.cargar_combine_draft()

# 2 — modelo de ronda (nd / r1 / r2)
X_ronda, y_ronda, features, le_posicion, le_ronda = fn.preparar_features_ronda(ncaa)
modelo_ronda = fn.entrenar_modelo_ronda(X_ronda, y_ronda)

# 3 — modelo de rango de pick (solo drafteados)
X_pick, y_pick, le_pick = fn.preparar_features_pick(ncaa, features)
modelo_pick = fn.entrenar_modelo_pick(X_pick, y_pick)

# 4 — clustering de arquetipos físicos
km, escalado, df_arquetipos = fn.entrenar_clustering(df_arquetipos)

# 5 — exporto todo a modelos/
fn.exportar_modelos(
    modelo_ronda, modelo_pick, km, escalado,
    le_posicion, le_ronda, le_pick, features, df_arquetipos
)
