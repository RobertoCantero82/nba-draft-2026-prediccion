# main.py
# orquesta todo el flujo: cargo modelos, predigo y muestro resultados

from config import JUGADORES
from modelos import cargar_modelos, predecir
from visualizacion import mostrar_resultados, mostrar_tabla_resumen, mostrar_grafico


def main():
    # cargo los modelos y sus codificadores
    modelo_ronda, le_ronda, modelo_rango, le_rango = cargar_modelos()

    # recorro cada jugador, muestro su prediccion y guardo el resultado
    resultados = []
    for jugador in JUGADORES:
        probs_ronda = predecir(jugador, modelo_ronda, le_ronda)
        probs_rango = predecir(jugador, modelo_rango, le_rango)
        mostrar_resultados(jugador, probs_ronda, probs_rango)
        resultados.append((jugador, probs_ronda, probs_rango))

    # muestro la tabla resumen y el grafico final con los tres juntos
    mostrar_tabla_resumen(resultados)
    mostrar_grafico(resultados)


if __name__ == "__main__":
    main()
