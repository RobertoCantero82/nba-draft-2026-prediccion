# config.py
# aqui centralizo las rutas, las constantes y los datos de los jugadores
# (todo lo que es "configuracion y datos", separado de la logica)

from pathlib import Path

# carpeta de este script (codigo/) y carpeta de modelos (pkl/ en la raiz del proyecto)
CARPETA_CODIGO = Path(__file__).resolve().parent
CARPETA_PKL = CARPETA_CODIGO.parent / "pkl"

# ruta donde guardo el grafico final
RUTA_GRAFICO = CARPETA_CODIGO / "prediccion_espanoles.png"

# estadisticas que necesitan los modelos sin posicion
ESTADISTICAS = ["pts", "treb", "ast", "stl", "blk"]

# orden fijo para mostrar siempre los rangos de pick igual
RANGOS_ORDEN = ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "ND"]

# estadisticas de los tres españoles (temporada 2025-26)
JUGADORES = [
    {"nombre": "Aday Mara",        "mock": "~#9",  "color": "#1d6fa4",
     "pts": 12.1, "treb": 6.8,  "ast": 0.9, "stl": 0.4, "blk": 2.6},
    {"nombre": "Baba Miller",      "mock": "~#45", "color": "#e07b39",
     "pts": 13.0, "treb": 10.3, "ast": 1.2, "stl": 0.8, "blk": 0.9},
    {"nombre": "Sergio de Larrea", "mock": "~#40", "color": "#2ecc71",
     "pts": 9.5,  "treb": 3.1,  "ast": 4.2, "stl": 1.1, "blk": 0.2},
]
