# VMetaFlow: A Meta-Framework for Integrating Visualizations in Coordinated View Applications
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
stages=["Data","Process","View","Decision"]

# Plot:
fig,ax=plt.subplots(figsize=(9,4)); ax.axis("off"); xs=np.linspace(.12,.88,4)
for k,(x,s) in enumerate(zip(xs,stages)):
    ax.text(x,.5,s,ha="center",va="center",bbox=dict(boxstyle="round",facecolor="white",edgecolor="black"))
    if k<3: ax.annotate("",(xs[k+1]-.07,.5),(x+.07,.5),arrowprops=dict(arrowstyle="->",lw=2))

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_11_improved.png", dpi=300, bbox_inches="tight")
plt.show()
