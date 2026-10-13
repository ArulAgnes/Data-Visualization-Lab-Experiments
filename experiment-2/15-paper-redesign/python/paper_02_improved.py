# The efficacy of stacked bar charts in supporting single-attribute and overall-attribute comparisons
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
cats=["A","B","C","D"]; a=np.array([4,3,5,2]); b=np.array([3,5,2,4])

# Plot:
fig,ax=plt.subplots(figsize=(9,5)); x=np.arange(4); w=.35
ax.bar(x-w/2,a,w,label="Attribute 1"); ax.bar(x+w/2,b,w,label="Attribute 2")
ax.set_xticks(x,cats); ax.set_ylabel("Illustrative comparison value"); ax.legend(frameon=False)

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_02_improved.png", dpi=300, bbox_inches="tight")
plt.show()
