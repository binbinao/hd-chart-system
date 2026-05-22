# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install pyswisseph fastapi uvicorn pydantic sqlalchemy pytest

# Run all tests
pytest tests/

# Run a single test class
pytest tests/test_calculator.py::TestRobinChart

# Run a single test
pytest tests/test_calculator.py::TestRobinChart::test_type_is_generator_family

# Start the API server (port 18090)
python -m hd_api.main
# Web UI: http://localhost:18090
# Swagger docs: http://localhost:18090/docs
```

## Architecture

This is a Human Design chart calculation system with four layers that flow top-to-bottom:

```
CalculateRequest → hd_calc → ChartResult → hd_interp → reading dict
                                         → hd_render → SVG string
                                         → hd_api    → REST endpoints
```

**Data flow**: Birth data → Julian Day → pyswisseph planet positions → gate/line mapping → channel/center/type/authority analysis → final `ChartResult` dataclass.

### Key modules

- **`hd_constants.py`** — Single source of truth for all HD system data: gate order (I Ching wheel at 302° offset), center definitions, channel mappings, type determination rules, authority priority, incarnation cross lookup tables. All other modules import from here.
- **`hd_calc/calculator.py`** — Core astronomical calculation. Uses `pyswisseph` Moshier ephemeris (no external .se1 files needed). The critical `find_design_date()` uses Newton-Raphson iteration to find when the Sun was 88° behind birth position. **Must use `FLG_SPEED` flag** or iteration won't converge.
- **`hd_calc/analysis.py`** — Derives higher-level HD properties from raw planet positions: finds channels (both gates present), determines defined centers (connected via complete channel), determines type (Generator/Manifestor/Projector/Reflector logic based on Sacral and motor-to-Throat connectivity via BFS), authority priority chain, definition type (single/split/triple/quadruple via BFS connected components), and incarnation cross lookup.
- **`adapters.py`** — Converts `ChartResult` dataclass → dict format expected by `hd_render`. Necessary because the renderer predates the dataclass models.
- **`hd_render/renderer.py`** — Generates SVG bodygraph. Gate positions are calculated as angular offsets around center perimeters. Channels colored by activation source (personality=black, design=red, both=striped).
- **`hd_interp/interpret.py`** — Assembles reading dict by looking up each chart element in the readings tables. Output is a nested dict, formatted by `formatter.py` into Markdown/JSON/plain text.
- **`hd_api/database.py`** — SQLite persistence via SQLAlchemy. Stores every chart calculation (birth data + full result JSON) in `hd_records.db`. Provides `save_record()` for writes and ORM model `ChartRecord` for queries. DB path configurable via `HD_DB_PATH` env var.

### Type determination logic (in `analysis.py`)

1. Sacral defined + motor reaches Throat → **Manifesting Generator**
2. Sacral defined, no motor-to-Throat → **Generator**
3. No Sacral, motor reaches Throat → **Manifestor**
4. No Sacral, no motor-to-Throat, has defined centers → **Projector**
5. No defined centers at all → **Reflector**

Motor-to-Throat connectivity uses BFS on the graph of centers connected by *activated channels* (not all possible bodygraph connections).

### HD wheel mapping

Ecliptic longitude → gate/line: subtract `WHEEL_OFFSET_DEGREES` (302°), divide by `GATE_SIZE_DEGREES` (5.625°), index into `GATE_ORDER[64]`. Line = subdivide gate segment into 6 equal parts.

## Conventions

- All modules use `sys.path.insert(0, ...)` to find project root — no package installation required.
- Data models are plain `@dataclass` classes (not Pydantic) in `hd_calc/models.py`; the API layer uses Pydantic `BaseModel` separately.
- Chinese and English names are always stored together (`name_zh`/`name_en` or `zh`/`en` keys).
- Reading text data lives in `hd_interp/readings/*.py` as plain Python dicts — no external data files.
- The API uses an in-memory LRU cache (max 256 entries) for computed readings.
- Every chart/reading calculation is automatically persisted to SQLite (`hd_records.db`). The database is created on first startup.
