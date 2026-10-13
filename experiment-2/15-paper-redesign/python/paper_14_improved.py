# Evaluation on interactive visualization data with scatterplots
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
x=np.arange(4); a=np.array([1,3,2,4]); b=np.array([2,4,1,3])

# Plot:
fig,axes=plt.subplots(1,3,figsize=(11,4))
for ax,off,title in zip(axes,[0,.25,.5],["View A","View B","View C"]):
    ax.scatter(x,a+off,s=55); ax.set_title(title); ax.set_ylim(0,5)

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_14_improved.png", dpi=300, bbox_inches="tight")
plt.show()
