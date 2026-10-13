# PCP-Ed: Parallel coordinate plots for ensemble data
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
rng=np.random.default_rng(10); data=np.cumsum(rng.normal(0,1,(80,5)),axis=0)

# Plot:
fig,ax=plt.subplots(figsize=(9,5))
for c in range(5): ax.plot(data[:,c],alpha=.12)
ax.plot(data.mean(axis=0),lw=3,marker="o"); ax.set_xticks(range(5),[f"Dim {k}" for k in range(1,6)])

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_10_improved.png", dpi=300, bbox_inches="tight")
plt.show()
