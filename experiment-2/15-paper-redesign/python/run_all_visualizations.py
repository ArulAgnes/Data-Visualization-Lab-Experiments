# Combined runner for all 15 educational visualization redesign scripts.
# Works no matter which folder you start Python from.
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
os.chdir(HERE)  # the scripts resolve their output folder from their own location

for script in sorted(HERE.glob("paper_*_improved.py")):
    print("running", script.name)
    exec(compile(script.read_text(encoding="utf-8"), str(script), "exec"))

print("done - figures written to", (HERE.parent / "visualizations"))
