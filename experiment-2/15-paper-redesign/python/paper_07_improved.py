# MalView: Interactive Visual Analytics for Comprehending Malware Behavior
# Educational reconstruction for M.E. CSE Data Visualization Exercise-2.
# The reconstruction is NOT a reproduction of the authors' research findings.
# Replace only with published numerical values when the source provides them.
import matplotlib.pyplot as plt
import numpy as np


import os
from pathlib import Path as _Path


def _visualizations_dir() -> _Path:
    """Where saved figures go: env override -> repo folder -> cwd fallback."""
    if os.environ.get("EX2_VIS_DIR"):
        out = _Path(os.environ["EX2_VIS_DIR"])
    else:
        try:
            out = _Path(__file__).resolve().parent.parent / "visualizations"
        except NameError:  # exec()'d inside a notebook cell: no __file__
            out = _Path.cwd() / "visualizations"
    out.mkdir(parents=True, exist_ok=True)
    return out


# Illustrative reconstruction data / structure:
views=["Supporting","Dynamic","Active analysis"]; priority=[4,6,8]

# Plot:
fig,ax=plt.subplots(figsize=(8,5)); ax.barh(views,priority); ax.invert_yaxis(); ax.set_xlabel("Illustrative attention priority")

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_07_improved.png", dpi=300, bbox_inches="tight")
plt.show()
