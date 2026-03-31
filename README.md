# Análisis de Datos Meteorológicos

> Proyecto final — Big Data · Grado en Matemáticas · UNIE Universidad

[![CI](https://github.com/PabloDelaFuenteArteaga/proyecto-meteorologia/actions/workflows/ci.yml/badge.svg)](https://github.com/PabloDelaFuenteArteaga/proyecto-meteorologia/actions/workflows/ci.yml)
[![Docs](https://github.com/PabloDelaFuenteArteaga/proyecto-meteorologia/actions/workflows/docs.yml/badge.svg)](https://PabloDelaFuenteArteaga.github.io/proyecto-meteorologia/)
[![Coverage](https://codecov.io/gh/PabloDelaFuenteArteaga/proyecto-meteorologia/graph/badge.svg)](https://codecov.io/gh/PabloDelaFuenteArteaga/proyecto-meteorologia)
[![Version](https://img.shields.io/github/v/release/PabloDelaFuenteArteaga/proyecto-meteorologia)](https://github.com/PabloDelaFuenteArteaga/proyecto-meteorologia/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

---

## Description

*Aplicación de técnicas de aprendizaje no supervisado (k-means, DBSCAN, clustering jerárquico) a series temporales meteorológicas para identificar y cartografiar regiones climáticas con comportamiento similar. El alumno deberá diseñar un vector de características climáticas para cada estación o punto de malla, y evaluar la calidad del clustering obtenido.*
## Documentation

Full documentation at **[PabloDelaFuenteArteaga.github.io/proyecto-meteorologia](https://PabloDelaFuenteArteaga.github.io/proyecto-meteorologia/)**

## Installation

  ```bash
  git clone https://github.com/PabloDelaFuenteArteaga/proyecto-meteorologia.git
  cd proyecto-meteorologia
  pip install uv
  uv sync --group dev
  ```

## Data Download

Data is not included in the repository. To download:

  ```bash
  # TODO: add your data download instructions
  ```

## Usage

  ```bash
  uv run pytest                          # run tests
  uv run pytest --cov=src -v     # tests with coverage
  uv run ruff check .                    # lint
  uv run ruff format .                   # format
  uv run mkdocs serve                    # preview docs at localhost:8000
  ```

## Project Structure

  ```
  proyecto-meteorologia/
  ├── .github/workflows/   # CI/CD pipelines
  ├── data/                # Data files (not committed — see .gitignore)
  ├── docs/                # MkDocs documentation sources
  ├── notebooks/           # Exploratory notebooks
  ├── src/weather/         # Source package
  ├── tests/               # Unit and integration tests
  ├── mkdocs.yml
  ├── pyproject.toml
  └── README.md
  ```

## Author

**Pablo De la Fuente Arteaga** · [github.com/PabloDelaFuenteArteaga](https://github.com/PabloDelaFuenteArteaga)

## Professor
**Álvaro Diez** · [github.com/alvarodiez20](https://github.com/alvarodiez20)

---

*Big Data · 4º Grado en Matemáticas · UNIE Universidad · 2025–2026*
