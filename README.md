# Particle Life Simulator

**Emergent behaviour from simple rules:** thousands of particles, one attraction/repulsion matrix, no central control. Clusters, cells and chasing swarms form on their own.

[![CI](https://github.com/41yannik/Particle-Life/actions/workflows/basic_ci.yml/badge.svg)](https://github.com/41yannik/Particle-Life/actions/workflows/basic_ci.yml)
![Python](https://img.shields.io/badge/python-3.10%E2%80%933.13-3776ab)
![Numba](https://img.shields.io/badge/Numba-JIT-00a3e0)
![Coverage](https://img.shields.io/badge/coverage-%E2%89%A570%25%20enforced-success)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<p align="center">
  <img src="docs/assets/particle-life.gif" width="400" alt="Particle Life simulation: coloured particle types forming clusters and swarms">
</p>

<p align="center"><sub>2,000 particles, 4 types, rendered headless from the simulation engine (<code>scripts/render_gif.py</code>, seed 3)</sub></p>

## Highlights

- **127x faster physics:** spatial hashing plus Numba JIT replaced the O(n²) brute-force engine. 1,000 particles went from 22.7 ms to 0.18 ms per step ([profiling report](docs/profiling_report.md)).
- **Real-time at scale:** the physics engine runs 1,222 steps per second at 2,000 particles. The OpenGL viewer (Vispy) renders that smoothly; the CPU-based Pygame viewer does not, and the [real-time verification](docs/realtime_verification.md) documents both.
- **Interactive controls:** change friction, force and interaction radius at runtime.
- **Engineering discipline:** CI on 3 operating systems × 4 Python versions, ruff, pytest with a 70 % coverage gate.

**Course:** Data Science & AI Infrastructures (winter 2025/26) · **Topic:** biology-inspired algorithms, emergent behaviour

---

## Project Overview

The **Particle Life Simulator** is an agent-based simulation engine designed to demonstrate how complex, organic-looking patterns (cellular structures, gliders, clusters) emerge from chaos without central orchestration.

The system simulates thousands of particles categorized into distinct types (colors). Their behavior is governed exclusively by a **forces matrix** defining attraction and repulsion rules between types within a limited radius.

**Core Inspiration:**
* [Jeffrey Ventrella's Clusters](http://www.ventrella.com/Clusters/)
* [Particle Life (Hunor Márton)](https://hunar4321.github.io/particle-life.html)

---

## Objectives & Scope

This project aims to deliver a production-grade Python application focusing on algorithmic efficiency and clean software architecture.

### 1. Core Simulation Engine
* **Interaction Matrix:** Implementation of an $N \times N$ matrix defining forces between at least **4 distinct particle types**.
* **Physics Logic:** Time-stepped calculation of velocity, friction, and acceleration based on distance thresholds ($r_{min}$, $r_{max}$).
* **Boundary Conditions:** Toroidal wrapping.

### 2. Performance Engineering
* **Optimization Target:** Real-time rendering of **>2,000 particles** at 60 FPS.
* **Profiling:** Continuous bottleneck analysis using `cProfile` and `timeit`.
* **Stack:** Utilization of **NumPy** for vectorized operations and potential JIT compilation via **Numba** to bypass Python interpreter overhead.

### 3. Visualization
* Real-time rendering pipeline (evaluated: `Vispy` vs `Pygame`).
* **GUI Controls:** Dynamic adjustment of interaction parameters (gravity, friction, range) during runtime.

### 4. Software Quality (QA/Ops)
* **CI/CD:** GitHub Actions pipeline for automated linting (`ruff`) and testing.
* **Testing Strategy:** Unit testing suite using `pytest` targeting >70% code coverage.
* **Standards:** Strict adherence to PEP-8 and Type Hinting.

## Software Architecture

The system is designed with a clear separation of concerns, orchestrated by a central controller (`main.py`) which manages the flow between configuration, simulation logic, and visualization.

### Architecture Diagram

```mermaid
flowchart TD
    A[main.py] --> B[config.py]
    A --> C[simulation.py]
    A --> D[viewer.py - pygame]
    A --> E[viewer_vispy.py - vispy]
    C --> F[physics.py]
    D --> C
    E --> C
    B --> C
    B --> D
    B --> E
```

### Module Breakdown:

* **Main Controller (`main.py`):** Entry point and mode dispatcher (`console`, `viewer`, `vispy`).
* **Configuration (`config.py`):** Central static parameters (window, physics constants, palette).
* **Simulation Engine (`simulation.py`):** Particle state, update loop, and interaction matrix usage.
* **Physics Kernel (`physics.py`):** Performance-critical force and movement calculations.
* **Pygame Viewer (`viewer.py`):** Interactive 2D viewer with runtime controls.
* **Vispy Viewer (`viewer_vispy.py`):** OpenGL-based viewer for better performance at higher particle counts.

---

## Roadmap

  * **[x] Milestone 1 (19.11.2025):** Project Setup, Architecture Design, CI Pipeline.
  * **[x] Milestone 2 (17.12.2025):** Core Logic Implementation (Physics & Interaction Matrix).
  * **[x] Milestone 3 (17.12.2025):** Real-time Visualization & Parameter Tuning.
  * **[x] Milestone 4 (Completed):** Performance Optimization (>2000 particles).
  * **[x] Milestone 5 (25.02.2026):** Final Release, Documentation & Presentation.

---

##  Local Development Setup

### Prerequisites

  * Python 3.10+
  * Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/41yannik/Particle-Life.git
cd Particle-Life

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the Simulation

```bash
# Console mode (headless, no window)
python -m particle_life.main

# Pygame viewer (interactive, CPU-based rendering)
python -m particle_life.main --mode viewer

# Vispy viewer (OpenGL, recommended for >1000 particles)
python -m particle_life.main --mode vispy
```

### Viewer Controls

Both viewers (Pygame and Vispy) use the same keyboard controls:

- `ESC`: Close the viewer
- `SPACE`: Pause/resume the simulation
- `F` / `G`: Increase / decrease friction
- `R` / `E`: Increase / decrease the global force factor
- `T` / `Z`: Increase / decrease the interaction radius

### Running Benchmarks & Profiling

```bash
# Profiling: Physics engine with cProfile + scaling analysis
python scripts/profile_simulation.py

# Side-by-side comparison: Brute-Force O(n²) vs. Spatial Hashing O(n)
python scripts/compare_engines.py

# Pygame FPS benchmark (measures rendering performance)
python scripts/test_pygame_fps.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=particle_life --cov-report=term-missing

# Run linter
ruff check
```

### Dependencies

Runtime:

- `numpy` – vectorized physics and linear algebra
- `pygame` – real-time visualization
- `vispy` – OpenGL-accelerated visualization backend
- `PyQt5` – Qt backend used by vispy on desktop

Development and CI:

- `pytest` – unit tests
- `pytest-cov` – coverage measurement and CI threshold
- `ruff` – linting

---

##  Team

  * **Arian Sharifi-Tabar**
  * **Yannik Huber**
  * **Wayan Schmidt**
  * **Azad Aygün**

### My role (Yannik Huber)

- set up the repository, the `ParticleSystem` core on NumPy arrays and the interaction matrix
- central configuration management (`config.py`), `pyproject.toml` packaging and CI fixes
- unit tests for simulation and interaction matrix
- English docstrings, final documentation and this README

## License

[MIT](LICENSE)
