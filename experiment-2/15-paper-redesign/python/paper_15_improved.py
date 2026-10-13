# Comparative eye-tracking evaluation of scatterplots and parallel coordinates
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
dims=[2,4,6,8]; scatter=[.80,.76,.68,.60]; pcp=[.72,.74,.78,.84]

# Plot:
fig,ax=plt.subplots(figsize=(8,5)); x=np.arange(len(dims)); w=.35
ax.bar(x-w/2,scatter,w,label="Scatterplots"); ax.bar(x+w/2,pcp,w,label="Parallel coordinates")
ax.set_xticks(x,dims); ax.set_xlabel("Number of dimensions"); ax.set_ylabel("Illustrative task accuracy"); ax.legend(frameon=False)

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_15_improved.png", dpi=300, bbox_inches="tight")
plt.show()
