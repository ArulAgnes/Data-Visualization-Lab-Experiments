"""Build the Kaggle-ready notebook for Experiment 2.

Reads the real exercise material (selection table + the 15 improved redesign
scripts + the three exercise visualizations) and emits a self-contained,
executed-from-source notebook:

    EXPERIMENT 2 - Research Visualization Redesign.ipynb

Every code cell is generated from the actual Python files in this folder, so
the notebook cannot drift away from the validated scripts.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "15-paper-redesign" / "python"
TABLE = ROOT / "15-paper-redesign" / "15_paper_selection_table.csv"
OUT_NOTEBOOK = ROOT / "EXPERIMENT 2 - Research Visualization Redesign.ipynb"

PRINCIPLES = """### Redesign principles applied

| # | Principle | What it changes |
|---|-----------|-----------------|
| 1 | **Reduce non-data ink** | Decorative borders, heavy frames and redundant gridlines are dropped so the data carries the chart. |
| 2 | **Direct labelling** | Values sit next to their marks instead of being deferred to a distant legend. |
| 3 | **One clear reading order** | Grouping and spacing tell the eye where to start and where to go next. |
| 4 | **Restrained, consistent colour** | Colour encodes meaning (category / condition) rather than decoration. |
| 5 | **Titles that state the takeaway** | The title answers "what should I notice?" instead of only naming the variables. |"""


def md(source: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(source.strip() + "\n")


def code(source: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(source.rstrip() + "\n")


def load_papers() -> list[dict]:
    with TABLE.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def split_exercise_script(path: Path) -> list[str]:
    """Split the three-exercise script into one source block per visualization."""
    text = path.read_text(encoding="utf-8")
    blocks, current = [], []
    for line in text.splitlines():
        if line.startswith("# VISUALIZATION") and current:
            blocks.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return blocks


def main() -> None:
    papers = load_papers()
    nb = nbf.v4.new_notebook()
    cells: list[nbf.NotebookNode] = []

    cells.append(
        md(
            """
# Experiment 2 — Research Visualization Redesign (EXERCISE-2)

**Course:** M.E. CSE — Data Visualization Lab
**Task:** take fifteen published research-paper figures, identify the visual
design problems that make them hard to read, and rebuild them as clear,
honest Python/Matplotlib visualizations.

| | |
|---|---|
| **Inputs** | `15-paper-redesign/15_paper_selection_table.csv` (paper, source, year, chart type, redesign problem) |
| **Scripts** | `15-paper-redesign/python/paper_01_improved.py` … `paper_15_improved.py` (one per paper) |
| **Runner** | `15-paper-redesign/python/run_all_visualizations.py` |
| **Exercise data** | `python/research_visualization_redesigns.py` (three EXERCISE-2 figures) |
| **Outputs** | `visualizations/paper_XX_improved.png` — on Kaggle: `/kaggle/working/visualizations` |

> **Academic-integrity note.** Original research figures are identified by paper
> and figure number. Where exact numerical values were not available in the
> accessible text or tables, the redesign is an *educational / conceptual
> reconstruction*: it does **not** claim to reproduce the authors' empirical
> results. The improved figures are original Python-generated designs.
"""
        )
    )

    cells.append(
        md(
            """
## 1. Environment

The notebook is fully self-contained: it only needs `numpy` and
`matplotlib`, both of which ship with the Kaggle Python runtime.
"""
        )
    )

    cells.append(
        code(
            """
import os
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Every figure this notebook saves goes here (works locally and on Kaggle).
os.environ.setdefault("EX2_VIS_DIR", str(Path.cwd() / "visualizations"))
VIS_DIR = Path(os.environ["EX2_VIS_DIR"])
VIS_DIR.mkdir(parents=True, exist_ok=True)

print("Python      :", sys.version.split()[0])
print("NumPy       :", np.__version__)
print("Matplotlib  :", matplotlib.__version__)
print("Figure output:", VIS_DIR)
"""
        )
    )

    cells.append(
        md(
            """
## 2. EXERCISE-2 visualizations

Three figures belonging to the exercise itself (comprehension score,
decision intention, presentation preference), plotted from the published
summary statistics. Raw scores are on a 0–6 scale; percentages are of
participants choosing each format.
"""
        )
    )

    exercise_blocks = split_exercise_script(ROOT / "python" / "research_visualization_redesigns.py")
    exercise_titles = [
        "**Trial A — mean comprehension score (0–6).** Horizontal bars with the standard deviation as an error bar; the value labels sit next to the bar so no legend lookup is needed.",
        "**Trial A — decision intention before vs after.** Grouped bars make the before/after comparison a distance the eye can measure directly.",
        "**Visual presentation preference.** Percentage bars with the share written at the end of each bar — one unit (per cent) for every mark.",
    ]
    for title, block in zip(exercise_titles, exercise_blocks):
        cells.append(md(title))
        cells.append(code(block))

    cells.append(
        md(
            f"""
## 3. Fifteen research-paper redesigns

{PRINCIPLES}

Each entry below pairs the paper with the redesign problem recorded for it and
the script that rebuilds the figure. The scripts write
`paper_XX_improved.png` into `VIS_DIR` and then render the figure inline.
"""
        )
    )

    for i, paper in enumerate(papers, start=1):
        slug = f"{i:02d}"
        cells.append(
            md(
                f"""
#### {slug}. {paper['Paper']}

*{paper['Source']}, {paper['Year']}* — chart type: **{paper['Visualization']}**

**Redesign problem.** {paper['Redesign Problem']}
"""
            )
        )
        script = SCRIPTS / f"paper_{slug}_improved.py"
        cells.append(code(script.read_text(encoding="utf-8")))
        cells.append(
            code(
                """
from IPython.display import Image, display
saved = VIS_DIR / "__NAME__"
size = saved.stat().st_size if saved.exists() else 0
print("__NAME__ ->", saved, f"({size:,} bytes)" if saved.exists() else "(not written)")
if saved.exists():
    display(Image(filename=str(saved), width=780))
""".replace("__NAME__", f"paper_{slug}_improved.png")
            )
        )

    cells.append(
        md(
            """
## 4. Output gallery

All fifteen regenerated figures, read back from the figure folder.
"""
        )
    )
    cells.append(
        code(
            """
from IPython.display import Image, display

improved = sorted(VIS_DIR.glob("paper_*_improved.png"))
print(f"{len(improved)} regenerated figure(s) in {VIS_DIR}")
for path in improved:
    print(" -", path.name, f"({path.stat().st_size:,} bytes)")
"""
        )
    )

    cells.append(
        md(
            """
### Poor baseline vs. redesigned figure

The package ships one `paper_XX_poor.png` baseline per paper. Those baselines
are **authored artefacts of the exercise** — they are *not* regenerated by any
script, so they are only shown when the image files were uploaded alongside the
notebook. When they are missing, the notebook says so instead of pretending.
"""
        )
    )
    cells.append(
        code(
            """
from IPython.display import Image, display

search_dirs = [VIS_DIR, Path.cwd() / "visualizations", Path.cwd() / "15-paper-redesign" / "visualizations"]
poor_files = {}
for d in search_dirs:
    for p in sorted(d.glob("paper_*_poor.png")):
        poor_files.setdefault(p.name, p)

if not poor_files:
    print("No pre-authored poor-baseline PNGs in this runtime.")
    print("The 15 improved redesigns above are regenerated in full by this notebook.")
else:
    print(f"{len(poor_files)} poor-baseline figure(s) found")
    for name in sorted(poor_files):
        improved = VIS_DIR / name.replace("_poor", "_improved")
        print(f"\\n--- {name} (authored baseline) ---")
        display(Image(filename=str(poor_files[name]), width=760))
        if improved.exists():
            print(f"--- {improved.name} (regenerated by this notebook) ---")
            display(Image(filename=str(improved), width=760))
"""
        )
    )

    cells.append(
        md(
            """
## 5. Results

* **18 figures** produced in total: 3 EXERCISE-2 visualizations + 15 paper redesigns,
  all generated from Python source rather than hand-drawn.
* Every improved figure keeps **one unit per axis**, prints its **values directly on the
  marks**, and uses colour only where it carries meaning.
* Each of the fifteen redesigns names the specific readability problem it removes
  (dense multi-stage flow, segment misalignment, overplotted polylines, edge
  crossings, small-multiple density, …).
* The poor/research baselines remain available as authored evidence of the *before*
  state; they are never silently re-generated.

**Reproduce locally**

```bash
cd experiment-2/15-paper-redesign
python python/run_all_visualizations.py     # writes all 15 improved PNGs
python python/research_visualization_redesigns.py
```

**Sources** — `15_paper_selection_table.csv`, `research_paper_bibliography.txt`,
`paper_download_verification.csv`, and the EXERCISE-2 record documents in
`experiment-2/records/`.
"""
        )
    )

    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    }
    nbf.write(nb, OUT_NOTEBOOK)

    n_code = sum(1 for c in cells if c.cell_type == "code")
    print(f"wrote {OUT_NOTEBOOK} ({OUT_NOTEBOOK.stat().st_size:,} bytes, "
          f"{len(cells)} cells, {n_code} code)")


if __name__ == "__main__":
    main()
