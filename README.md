<div align="center">

![RC — NBA Draft 2026 ML Predictor](logo.gif)

</div>

---

## ¿De qué va esto?

El periodismo deportivo predice el Draft de la NBA cada año de la misma manera: opiniones de scouts, análisis subjetivos y "corazonadas" de expertos. Todos los artículos dicen lo mismo.

Este proyecto propone algo diferente: **usar Machine Learning para respaldar artículos periodísticos con datos objetivos**. Modelos entrenados con 13 años de estadísticas reales de la NCAA capaces de predecir si un jugador será elegido en el Draft, en qué ronda, en qué rango de pick y a qué perfil de jugador histórico se parece.

El caso de uso: los tres jugadores españoles con opciones reales en el **NBA Draft 2026**.

---

## 🎯 ¿Qué predice el modelo?

| Predicción | Pregunta | Tipo |
|---|---|---|
| **Ronda** | ¿Primera ronda / Segunda ronda / No drafteado? | Clasificación (3 clases) |
| **Rango de pick** | ¿En qué franja del 1 al 60? | Clasificación multiclase (6 rangos) |
| **Arquetipo** | ¿A qué perfil físico histórico se parece? | Clustering no supervisado |

---

## 🇪🇸 Los protagonistas

| Jugador | Posición | Liga | Mock Draft |
|---|---|---|---|
| **Aday Mara** | Pívot | Michigan (NCAA) | ~Top 15 |
| **Baba Miller** | Ala-Pívot | Cincinnati (NCAA) | ~Pick 32 |
| **Sergio De Larrea** | Base | Valencia Basket (EuroLeague) | ~Pick 40 |

---

## 📂 Estructura del repositorio

```
nba-draft-2026-prediccion/
│
├── datos/                        # Datasets del proyecto
│   ├── raw/                      # Fuentes originales sin procesar
│   └── procesados/               # Datasets limpios listos para el modelo
│
├── notebooks/                    # Análisis y desarrollo paso a paso
│
├── codigo/                       # Scripts Python reutilizables
│
├── modelos/                      # Modelos entrenados (.pkl)
│
├── app_streamlit/                # Aplicación web interactiva
│
├── documentacion/                # Memoria y documentación técnica
│
├── presentacion/                 # Presentaciones del proyecto
│
└── README.md
```

---

## 📊 Fuentes de datos

### NCAA Histórico → modelo de clasificación
- **Origen:** Kaggle — `College_BasketballPlayers2009-2021.csv`
- **Crudo:** 61.061 registros · 66 columnas · 209K NaN
- **Procesado:** 2.121 jugadores · 37 variables · 0 NaN
- 13 años de estadísticas universitarias: puntos, rebotes, BPM, eFG%, usage rate...

### NBA Draft Combine → clustering de arquetipos
- **Origen:** `nba_api` — Combine histórico 2000–2026
- **Crudo:** 1.873 registros · 47 columnas · 45K NaN
- **Procesado:** 1.873 jugadores · 18 columnas · 0 NaN
- Medidas físicas reales de Aday Mara, Baba Miller y Sergio De Larrea incluidas

### NBA Players Draft → etiquetado de arquetipos
- **Origen:** `nbaplayersdraft.csv`
- 1.922 jugadores con carreras NBA históricas
- Usado para asignar comparables reales a cada cluster

---

## ⚙️ Modelos

### Clasificación — Ronda
- **Target:** R1 / R2 / No drafteado
- **Candidatos:** XGBoost · Random Forest · SVM · KNN

### Clasificación — Rango de pick
- **Target:** 1-10 / 11-20 / 21-30 / 31-40 / 41-50 / 51-60
- **Candidatos:** XGBoost · Decision Tree · KNN · Random Forest

### Clustering — Arquetipo
- **Features:** datos físicos del Combine (altura, peso, envergadura, alcance, salto, agilidad)
- **Candidatos:** K-Means · DBSCAN
- **Output:** perfil de jugador + comparable histórico más cercano

---

## 🛠️ Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-189AB4?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)

---

## 👤 Autor

**Roberto Cantero** · [@RobertoCantero82](https://github.com/RobertoCantero82)
