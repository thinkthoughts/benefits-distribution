from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
RESULTS = ROOT / "results"
DATA = ROOT / "data"
NOTEBOOKS = ROOT / "notebooks"

for path in [FIGURES, RESULTS, DATA, NOTEBOOKS]:
    path.mkdir(parents=True, exist_ok=True)
