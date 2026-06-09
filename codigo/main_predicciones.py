# main_predicciones.py
# pide datos de un jugador por consola y devuelve:
#   → si será drafteado, la ronda y el rango de pick
#   → su arquetipo físico y los comparables históricos y actuales
# ejecutar desde la carpeta codigo/: python main_predicciones.py

import funciones as fn

# posiciones que el modelo conoce (las del dataset de entrenamiento)
POSICIONES_VALIDAS = [
    'C', 'PF/C', 'Wing F', 'Wing G',
    'Combo G', 'Scoring PG', 'Pure PG', 'Stretch 4', 'desconocido'
]

# 1 — cargo los modelos desde disco
m = fn.cargar_modelos()

# 2 — pido el nombre del jugador
print("\n🏀 NBA DRAFT 2026 — predictor de jugadores")
print("─" * 45)
nombre = input("nombre del jugador: ").strip()

# 3 — pido stats de juego y predigo draft
stats = fn.pedir_stats_juego(POSICIONES_VALIDAS)

# adapto altura_cm al formato que espera el modelo (se llama altura_cm en ncaa)
stats['altura_cm'] = stats.pop('altura_cm', stats.get('altura_cm'))

resultado_draft = fn.predecir_draft(stats, m)
fn.mostrar_resultado_draft(nombre, resultado_draft)

# 4 — pido físicas y predigo arquetipo + comparables
print("\n── a continuación introduce las medidas físicas para el arquetipo ──")
fisicas = fn.pedir_fisicas()

arquetipo, historicos, activos = fn.predecir_arquetipo(fisicas, m)
fn.mostrar_resultado_arquetipo(nombre, arquetipo, historicos, activos)
