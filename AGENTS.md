# Repository Guidelines

## Project Overview

Full-stack Human Design (HD) chart calculation system in Python. Computes HD charts from birth data (planetary positions via Swiss Ephemeris → gate/line mapping → type/authority/profile analysis), generates Chinese-language interpretations, renders SVG bodygraphs, and serves everything through a FastAPI REST API with a single-page web UI. AI-powered deep readings stream from any OpenAI-compatible API.

## Architecture & Data Flow

Four layers, strictly top-to-bottom:

```
ChartRequest (Pydantic, hd_api)
  → hd_calc.calculate_chart()          # astronomy + analysis → ChartResult dataclass
  → hd_interp.generate_reading()       # ChartResult → nested reading dict
  → hd_render.render_bodygraph()       # render dict (via adapters.py) → SVG string
  → hd_api                             # REST endpoints, SQLite persistence, SSE AI stream
```

**Calculation pipeline** (`hd_calc/calculator.py`): birth data → `swe.julday()` → personality positions → `find_design_date()` (Newton-Raphson: Sun exactly 88° of *ecliptic longitude* behind birth Sun, NOT 88 days; initial guess `birth_jd − 88/0.9856`, convergence 1e-8, max 50 iterations) → design positions → `analyze_chart()`.

**Analysis rules** (`hd_calc/analysis.py`):
- Channel active iff **both** gates present in union of personality+design gate sets.
- Center defined iff it participates in a **complete activated channel** (single activated gate never defines a center).
- Type via ordered chain: no defined centers → Reflector; Sacral + motor→Throat → Manifesting Generator; Sacral → Generator; motor→Throat → Manifestor; else Projector.
- Motor→Throat connectivity uses **BFS over activated-channel graph only** (indirect paths count; `CENTER_CONNECTIONS` is NOT the traversal graph). Definition type (single/split/triple/quadruple) also uses BFS connected components on the same graph.

## Key Directories

| Directory | Purpose |
|---|---|
| `hd_calc/` | Astronomy (`calculator.py`), HD analysis (`analysis.py`), plain `@dataclass` models (`models.py`) |
| `hd_interp/` | `interpret.py` builds reading dict; `formatter.py` (markdown/json/plain); `readings/*.py` hold all reading text as Python dicts |
| `hd_render/` | `renderer.py` SVG bodygraph; `styles.py` canvas/position/color constants |
| `hd_api/` | FastAPI app, entry point, SQLite persistence, AI service, DI layer, static web UI |
| `tests/` | Single pytest file covering hd_calc + hd_constants |

## Development Commands

```bash
# Install (no lockfile; floor-pinned >= constraints)
pip install -r requirements.txt

# Run tests
pytest tests/
pytest tests/test_calculator.py::TestRobinChart                      # one class
pytest tests/test_calculator.py::TestRobinChart::test_type_is_generator_family  # one test

# Run API server (port 18090; Web UI at http://localhost:18090, Swagger at /docs)
python -m hd_api.main

# Container / deploy
docker build -t hd-chart-system .   # python:3.11-slim; CMD python -m hd_api.main
fly deploy                          # fly.io, region hkg, volume hd_data → /data
```

No linter/formatter configuration exists. No CI, Makefile, or pyproject.toml.

## Code Conventions & Common Patterns

- **Two model systems, deliberately**: internal data models are plain `@dataclass` (`hd_calc/models.py`); Pydantic `BaseModel` only at the API boundary (`ChartRequest` in `hd_api/app.py`). `app.py:_chart_to_dict()` does manual dataclass→dict serialization.
- **No package installation** — every non-root module bootstraps with `sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))` (~5 files). New modules outside the root must follow this.
- **`hd_constants.py` is the single source of truth** for all HD data: `WHEEL_OFFSET_DEGREES=302.0`, `GATE_SIZE_DEGREES=5.625`, `GATE_ORDER[64]`, `CHANNELS` (36, keys are `(smaller, larger)` gate tuples), `GATE_INFO`, `TYPES` (key `'ManifestingGenerator'`, no space), `AUTHORITY_PRIORITY`, cross/name tables. Never duplicate these values elsewhere.
- **Ephemeris flags are load-bearing**: all `swe.calc_ut` calls must use `FLG_MOSEPH | FLG_SPEED`. Without `FLG_SPEED` the speed component is zero and `find_design_date()` diverges. Moshier ephemeris means no `.se1` files ever.
- **Adapter layer**: `adapters.py:chart_to_render_dict()` bridges `ChartResult` → plain dict because `renderer.py` predates the dataclasses and expects `{planet: (longitude, gate, line)}` tuples. Called only by `/bodygraph`.
- **Bilingual fields everywhere**: `name_zh`/`name_en` on dataclasses and `'zh'`/`'en'` keys in constants dicts — always store both together.
- **Channel lookups try both orderings**: `(g1,g2)` then `(g2,g1)` — replicate in any new channel lookup (see `interpret.py`, `dependencies.py`, `app.py`).
- **Error handling**: API endpoints wrap in try/except → `HTTPException(500, str(e))`; 404 for missing cache/records/gates/channels/types; 400 for out-of-range gate numbers; 503 for unconfigured AI. No custom exception classes. AI streaming errors are yielded as SSE events, not raised.
- **State management**: in-memory LRU reading cache (`app.py`, `OrderedDict`, max 256, md5-of-params key, lost on restart — only `/reading` populates it) + SQLite persistence of every calculation (`hd_records.db`, no dedup). Cache and DB are independent.

## Important Files

| File | Role |
|---|---|
| `hd_constants.py` | All HD system data; imported by every layer |
| `hd_calc/calculator.py` | `calculate_chart()`, `degree_to_gate_line()`, `find_design_date()` |
| `hd_calc/analysis.py` | `analyze_chart()` + `_determine_*` functions (type/authority/profile/definition/cross) |
| `adapters.py` | `chart_to_render_dict()` — dataclass → renderer dict |
| `hd_interp/interpret.py` | `generate_reading()` → 9-section reading dict |
| `hd_api/app.py` | All 11 REST endpoints, cache, `_chart_to_dict()` |
| `hd_api/main.py` | Entry point: `load_dotenv()` → uvicorn |
| `hd_api/database.py` | `ChartRecord` ORM, `init_db()`, `get_db()`, `save_record()` |
| `hd_api/ai_service.py` | `stream_ai_reading()` SSE generator, `get_ai_config()` |
| `hd_api/dependencies.py` | DI layer: `do_calculate`, `do_reading`, `get_*_info` |
| `hd_api/static/index.html` | Single-file SPA web UI (zh-CN, calls `/reading`, `/bodygraph`, `/ai-reading`) |
| `requirements.txt` | 8 floor-pinned deps (pyswisseph, fastapi, uvicorn, pydantic, sqlalchemy, openai, python-dotenv, pytest) |
| `Dockerfile` / `fly.toml` | python:3.11-slim single-stage; Fly.io hkg region, 512MB, `/data` volume |

**REST endpoints**: `POST /chart`, `POST /reading`, `GET /reading/{chart_id}`, `GET /gate/{n}`, `GET /channel/{g1}/{g2}`, `POST /bodygraph`, `GET /type/{name}`, `GET /records` (paginated), `GET /records/{id}`, `GET /ai-config`, `POST /ai-reading` (SSE).

## Runtime/Tooling Preferences

- **Python 3.11** (Docker base `python:3.11-slim`); `gcc` needed at install time for pyswisseph's C extension.
- **pip** with `requirements.txt`; no lockfile, no virtualenv tooling pinned.
- **Env vars** (all loaded via python-dotenv; see `.env.example`):

| Var | Default | Notes |
|---|---|---|
| `PORT` | `18090` | Fly sets `8080` |
| `HD_DB_PATH` | `hd_records.db` (CWD-relative) | Docker/Fly set `/data/hd_records.db` |
| `AI_API_KEY` | `''` | Required only for AI features; empty → `get_ai_config()` reports unconfigured |
| `AI_BASE_URL` | `https://api.openai.com/v1` | Any OpenAI-compatible endpoint works |
| `AI_MODEL` | `gpt-4o` | |

- CORS allows all origins; server binds `0.0.0.0`, `reload=False`.

## Testing & QA

- **pytest only**, no plugins, no config files (no `pytest.ini`/`conftest.py`/markers), no coverage tooling.
- Single file `tests/test_calculator.py`: 6 classes, ~37 tests. Chart classes (`TestRobinChart`, `TestManifestorChart`, `TestProjectorChart`) define per-class `chart` fixtures with hardcoded birth data and exercise **real pyswisseph calculations** (no mocks). Pure-function classes (`TestDegreeToGateLine`, `TestIncarnationCross`) test math and constants tables directly.
- Conventions: classes `Test<Subject>`, methods `test_<behavior>` snake_case.
- **Coverage gaps**: `hd_render/`, `hd_interp/`, `adapters.py`, and all of `hd_api/` have zero tests. Verify API changes by launching the server and hitting endpoints; verify renderer changes by inspecting generated SVG.
- Tests import via the same `sys.path.insert` bootstrap as source modules.
