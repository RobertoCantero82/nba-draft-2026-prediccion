# visualizacion.py
# aqui dejo todo lo que muestra resultados: por pantalla y en grafico

import matplotlib.pyplot as plt

from config import RANGOS_ORDEN, RUTA_GRAFICO
from modelos import prob_draft


def mostrar_resultados(jugador, probs_ronda, probs_rango):
    # busco la ronda y el rango mas probables
    ronda_top = max(probs_ronda, key=probs_ronda.get)
    rango_top = max(probs_rango, key=probs_rango.get)
    # imprimo la cabecera del jugador
    print(f"\n{'=' * 55}")
    print(f"  {jugador['nombre']}  (mock {jugador['mock']})")
    print(f"{'=' * 55}")
    print(f"  Probabilidad de ser drafteado: {prob_draft(probs_ronda):.1f}%")
    print(f"  Ronda mas probable:            {ronda_top}")
    print(f"  Rango de pick mas probable:    {rango_top}")
    # muestro el detalle de probabilidades por ronda
    print("\n  Detalle por ronda:")
    for clase in probs_ronda:
        print(f"    {clase:<4} {probs_ronda[clase] * 100:5.1f}%")
    # muestro el detalle de probabilidades por rango, en orden fijo
    print("\n  Detalle por rango de pick:")
    for rango in RANGOS_ORDEN:
        if rango in probs_rango:
            print(f"    {rango:<6} {probs_rango[rango] * 100:5.1f}%")


def mostrar_tabla_resumen(resultados):
    # imprimo una tabla compacta con los tres jugadores juntos
    print(f"\n{'=' * 60}")
    print("  RESUMEN FINAL")
    print(f"{'=' * 60}")
    print(f"  {'Jugador':<18}{'P(draft)':>10}{'Ronda':>8}{'Rango':>10}")
    print(f"  {'-' * 46}")
    for jugador, probs_ronda, probs_rango in resultados:
        # ronda y rango mas probables de cada jugador
        ronda_top = max(probs_ronda, key=probs_ronda.get)
        rango_top = max(probs_rango, key=probs_rango.get)
        print(f"  {jugador['nombre']:<18}{prob_draft(probs_ronda):>9.1f}%{ronda_top:>8}{rango_top:>10}")


def mostrar_grafico(resultados, ruta_salida=RUTA_GRAFICO):
    # creo una figura con un panel por jugador
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#0a1019")
    fig.suptitle("NBA Draft 2026 — Predicción por rango de pick",
                 color="white", fontsize=15, y=1.02)

    for ax, (jugador, probs_ronda, probs_rango) in zip(axes, resultados):
        # ordeno las probabilidades de rango segun el orden fijo (en %)
        valores = [probs_rango.get(rango, 0) * 100 for rango in RANGOS_ORDEN]
        # destaco el rango mas probable con el color del jugador y dejo el resto en gris
        rango_top = RANGOS_ORDEN[valores.index(max(valores))]
        colores = [jugador["color"] if rango == rango_top else "#3a4658" for rango in RANGOS_ORDEN]
        # pinto las barras sobre fondo oscuro
        ax.set_facecolor("#0a1019")
        barras = ax.bar(RANGOS_ORDEN, valores, color=colores, alpha=0.9)
        # escribo el porcentaje encima de cada barra con algo de altura
        for barra, valor in zip(barras, valores):
            if valor > 1:
                ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 1,
                        f"{valor:.0f}%", ha="center", va="bottom", color="white", fontsize=9)
        # titulo con nombre, mock y probabilidad de draft
        ax.set_title(f"{jugador['nombre']}  (mock {jugador['mock']})\nP(draft) = {prob_draft(probs_ronda):.0f}%",
                     color="white", fontsize=11)
        ax.set_ylim(0, max(valores) + 15)
        ax.set_ylabel("Probabilidad (%)", color="white")
        ax.tick_params(colors="white")
        # giro las etiquetas del eje x para que se lean bien
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        for spine in ax.spines.values():
            spine.set_edgecolor("#ffffff22")

    plt.tight_layout()
    # guardo el grafico en un png y lo muestro por pantalla
    plt.savefig(ruta_salida, dpi=130, facecolor="#0a1019", bbox_inches="tight")
    plt.show()
    print(f"\nGrafico guardado en: {ruta_salida}")
