# Habitabilidad Casa-Transporte 🏡🚗

### Sistema de Análisis Optimización de Rutas Urbanas


## Introduction

**Habitabilidad Casa-Transporte** es una aplicación de análisis espacial desarrollada en Python para evaluar la **habitabilidad de zonas residenciales** según las restricciones de movilidad urbana. El sistema analiza los trayectos desde un punto origen (Punto A 📍) hacia un destino diario habitual (Punto B 📍, como trabajo o universidad), procesando variables críticas como tiempo de desplazamiento (en horas), costo de combustible y distancia total.

A través del desacoplamiento entre y interpolacion y suposicion de varias variables, el procesamiento topológico de grafos, la evaluación matricial y la renderización interactiva, esta herramienta proporciona un mapa interactivo en el que podras ver con capas de calor para identificar las mejores zonas para vivir y las rutas ideales.

---

## Installation

Sigue estos pasos para configurar el entorno de desarrollo e instalar las dependencias con **`uv`**.

### Prerequisites

Antes de ejecutar la aplicación, asegúrate de contar con lo siguiente:

**Python 3.10 o superior:** Requerido para el procesamiento vectorial y manejo de grafos.

**Gestor de Paquetes `uv`:** Herramienta de gestión de paquetes y entornos de alto rendimiento.

**OpenStreetMap Access:** Conexión a internet para la descarga de mallas viales mediante la API de Overpass / OSMnx.

**Navegador Web:** Para abrir y visualizar el mapa interactivo generado (`.html`).

---

## 📦 Project Structure & Directory Tree

El proyecto está estructurado usando la disposición estándar de paquetes de **`uv`**, separando los módulos por responsabilidad:

```text
habitabilidad-casa-transporte/
├── pyproject.toml
├── uv.lock
├── README.md
├── sources/                          # Recurso de imágenes y assets del README
│   └── Image/
│       └── readme/
└── src/
    └── habitabilidad_casa_transporte/


El proyecto sigue un flujo desacoplado que va desde la descarga de la red vial hasta la representación interactiva de datos:

graph TD
    %% Style Definitions
    classDef fetcher fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px,color:#000;
    classDef logic fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#000;
    classDef eval fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#000;
    classDef view fill:#eceff1,stroke:#607d8b,stroke-width:2px,color:#000;

    %% Components
    OSM[(OpenStreetMap / Overpass)]:::view
    Fetcher[MapFetcher / OSMnx]:::fetcher
    Processor[GraphProcessor / NetworkX]:::logic
    Evaluator[HabitabilityEvaluator / NumPy]:::eval
    Visualizer[MapVisualizer / Folium]:::view
    Output[Mapa Interactivo HTML]:::view

    %% Relationships and Flow
    OSM -->|Descarga malla vial| Fetcher
    Fetcher -->|Entrega MultiDiGraph| Processor
    Processor -->|Calcula rutas y tiempos| Evaluator
    Evaluator -->|Genera matrices de habitabilidad| Visualizer
    Visualizer -->|Exporta capa gráfica| Output


    Lista completa de dependencias instaladas en el proyecto habitabilidad-casa-transporte v0.1.0:

    habitabilidad-casa-transporte v0.1.0
├── folium v0.20.0
│   ├── branca v0.8.2
│   │   └── jinja2 v3.1.6
│   │       └── markupsafe v3.0.3
│   ├── jinja2 v3.1.6 (*)
│   ├── numpy v2.5.3
│   ├── requests v2.34.2
│   │   ├── certifi v2026.7.22
│   │   ├── charset-normalizer v3.5.1
│   │   ├── idna v3.19
│   │   └── urllib3 v2.8.0
│   └── xyzservices v2026.9.1
├── networkx v3.6.1
└── osmnx v2.1.1
    ├── geopandas v1.1.4
    │   ├── numpy v2.5.3
    │   ├── packaging v26.3
    │   ├── pandas v3.0.5
    │   │   ├── numpy v2.5.3
    │   │   ├── python-dateutil v2.9.0.post0
    │   │   │   └── six v1.17.0
    │   │   └── tzdata v2026.4
    │   ├── pyogrio v0.13.0
    │   │   ├── certifi v2026.7.22
    │   │   ├── numpy v2.5.3
    │   │   └── packaging v26.3
    │   ├── pyproj v3.8.0
    │   │   └── certifi v2026.7.22
    │   └── shapely v2.1.2
    │       └── numpy v2.5.3
    ├── networkx v3.6.1
    ├── numpy v2.5.3
    ├── pandas v3.0.5 (*)
    ├── requests v2.34.2 (*)
    └── shapely v2.1.2 (*)


🚀 Getting Started
1. Clonar el repositorio

git clone []
cd habitabilidad-casa-transporte

2. Sincronizar el entorno virtual con uv
uv sync

3. Ejecutar el proyecto
uv run python -m habitabilidad_casa_transporte.main


🌟 Support the project
If this project improves your urban mobility analysis or development workflows, please give it a ⭐

⭐ Star · 🍴 Fork

This is an independent open-source project.