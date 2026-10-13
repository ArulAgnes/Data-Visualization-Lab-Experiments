# Toward automatic comparison of visualization techniques: Application to graph visualization
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
stages=["Generate","Train","Evaluate","Compare","Report"]

# Plot:
fig,ax=plt.subplots(figsize=(11,3.8)); ax.axis("off"); xs=np.linspace(.1,.9,5)
for k,(x,s) in enumerate(zip(xs,stages)):
    ax.text(x,.5,s,ha="center",va="center",bbox=dict(boxstyle="round",facecolor="white",edgecolor="black"))
    if k<4: ax.annotate("",(xs[k+1]-.06,.5),(x+.06,.5),arrowprops=dict(arrowstyle="->",lw=1.8))

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_04_improved.png", dpi=300, bbox_inches="tight")
plt.show()
